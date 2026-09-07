def generate_study_response(topic, prompt):
    prompt = (prompt or "").strip()

    if not prompt:
        return {
            "title": topic.title if topic else "Study Assistant",
            "response": (
                "Ask a question about your current learning topic. "
                "You can request an explanation, examples, revision notes, "
                "practice ideas, or a study plan."
            )
        }

    topic_name = topic.title if topic else "your topic"

    return {
        "title": f"Study guidance: {topic_name}",
        "response": (
            f"Here is a structured explanation for your request about "
            f"{topic_name}:\n\n"
            f"{prompt}\n\n"
            "Study approach:\n"
            "1. Understand the main concept.\n"
            "2. Review a practical example.\n"
            "3. Practice with a small exercise.\n"
            "4. Test yourself with a quiz.\n"
            "5. Schedule a focused revision session."
        )
    }
