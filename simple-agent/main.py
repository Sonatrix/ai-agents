from dotenv import load_dotenv

from src.agent import Agent


def main():
    print("Welcome to the Ollama Chat Agent! Type 'exit' to quit.")

    agent = Agent(system="You are a helpful assistant.")
    # Main loop for conversation handlin
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        # Get the agent's response
        response = agent.__call__(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    load_dotenv()
    main()
