import os
from dotenv import load_dotenv
import json
import importlib.util
from pathlib import Path
from anthropic import Anthropic

load_dotenv()

ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY")

class SkillsAgent:
    def __init__(self, skills_dir="skills"):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.skills_dir = Path(skills_dir)
        self.skills = self._load_skills()
    
    def _load_skills(self):
        """Load all skills from the skills directory"""
        skills = {}
        
        if not self.skills_dir.exists():
            return skills
        
        for skill_folder in self.skills_dir.iterdir():
            if not skill_folder.is_dir():
                continue
            
            skill_md = skill_folder / "SKILL.md"
            skill_py = skill_folder / f"{skill_folder.name}.py"
            
            if skill_md.exists() and skill_py.exists():
                # Load skill metadata
                skill_info = self._parse_skill_md(skill_md)
                
                # Load skill function
                spec = importlib.util.spec_from_file_location(
                    skill_folder.name, skill_py
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Get the main function (assumes first function in file)
                func_name = [name for name in dir(module) 
                           if callable(getattr(module, name)) 
                           and not name.startswith('_')][0]
                
                skills[skill_info['name']] = {
                    'info': skill_info,
                    'function': getattr(module, func_name)
                }
        
        return skills
    
    def _parse_skill_md(self, md_path):
        """Parse SKILL.md to extract metadata"""
        with open(md_path, 'r') as f:
            content = f.read()
        
        # Simple parser - you might want to use YAML or more robust parsing
        lines = content.strip().split('\n')
        skill_info = {'parameters': []}
        
        current_param = None
        for line in lines:
            line = line.strip()
            if line.startswith('name:'):
                skill_info['name'] = line.split('name:')[1].strip()
            elif line.startswith('description:'):
                skill_info['description'] = line.split('description:')[1].strip()
            elif '- name:' in line:
                if current_param:
                    skill_info['parameters'].append(current_param)
                current_param = {'name': line.split('name:')[1].strip()}
            elif current_param and 'type:' in line:
                current_param['type'] = line.split('type:')[1].strip()
            elif current_param and 'description:' in line:
                current_param['description'] = line.split('description:')[1].strip()
        
        if current_param:
            skill_info['parameters'].append(current_param)
        
        return skill_info
    
    def _skills_to_tools(self):
        """Convert skills to Anthropic tool format"""
        tools = []
        for skill_name, skill_data in self.skills.items():
            info = skill_data['info']
            tool = {
                "name": skill_name.lower().replace(' ', '_'),
                "description": info['description'],
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
            
            for param in info.get('parameters', []):
                tool['input_schema']['properties'][param['name']] = {
                    "type": param['type'],
                    "description": param.get('description', '')
                }
                tool['input_schema']['required'].append(param['name'])
            
            tools.append(tool)
        
        return tools
    
    def _execute_skill(self, skill_name, parameters):
        """Execute a skill function with given parameters"""
        for name, skill_data in self.skills.items():
            if name.lower().replace(' ', '_') == skill_name:
                try:
                    result = skill_data['function'](**parameters)
                    return result
                except Exception as e:
                    return {"error": str(e)}
        
        return {"error": f"Skill {skill_name} not found"}
    
    async def chat(self, user_message, max_turns=5):
        """Main chat loop with tool use"""
        messages = [{"role": "user", "content": user_message}]
        tools = self._skills_to_tools()
        
        print(f"Loaded {len(tools)} skills: {[t['name'] for t in tools]}\n")
        
        for turn in range(max_turns):
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )
            
            print(f"Turn {turn + 1}:")
            print(f"Stop reason: {response.stop_reason}\n")
            
            # Check if Claude wants to use a tool
            if response.stop_reason == "tool_use":
                # Add assistant's response to messages
                messages.append({"role": "assistant", "content": response.content})
                
                # Execute all tool calls
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"Using tool: {block.name}")
                        print(f"Parameters: {block.input}\n")
                        
                        result = self._execute_skill(block.name, block.input)
                        
                        print(f"Tool result: {result}\n")
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result)
                        })
                
                # Add tool results to messages
                messages.append({"role": "user", "content": tool_results})
            
            else:
                # Claude provided a final response
                for block in response.content:
                    if hasattr(block, 'text'):
                        print(f"Claude: {block.text}\n")
                
                return response.content[0].text
        
        print("Max turns reached")
        return response.content[0].text
