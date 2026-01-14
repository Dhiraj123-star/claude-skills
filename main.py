from  fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from skills_agent import SkillsAgent

app = FastAPI(
    title="Claude Skills API"
)

agent = SkillsAgent()

class Query(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {
        "status":"Agent is online",
        "skills_loaded":list(agent.skills.keys())
    }

@app.post("/ask")
async def ask_agent(query:Query):
    try:
        response= await agent.chat(query.text)
        return {"answer":response}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)