from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.yfinance import YFinanceTools

agent = Agent(
        model=Ollama(id="qwen3:4b"),
    tools=[YFinanceTools(stock_price=True)],
    markdown=True,
)
agent.print_response("What is the stock price of AAPL?", stream=True)
