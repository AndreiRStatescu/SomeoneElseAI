from src.services.openai_service import OpenAIService


def main():
    service = OpenAIService()

    result = service.generate_response(
        message="What is the capital of France?", mode="ask", model="gpt-5-nano"
    )

    print(f"Status: {result.get('status')}")
    if result.get("response"):
        print(f"Response: {result.get('response')}")
    else:
        print(f"Error: {result.get('error')}")
        if result.get("details"):
            print(f"Details: {result.get('details')}")


if __name__ == "__main__":
    main()
