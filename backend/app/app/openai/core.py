def ask(context, question, manager):
    prompt = f"""
    Answer the following question according to the provided context. If the context doesn't contain the answer, Do Not Answer!
    If the context doesn't mention anything about the qustion Please Say the The Question Is Out Of Context!
    If the context Is empty, Please Say No Context!

    context: {context}

    question: {question}

    answer:
    """

    return manager.get_chat_completion(prompt)


def ask_stream(context, question, messages, manager):
    prompt = f"""
    Answer the following question according to the provided context. If the context doesn't contain the answer, Do Not Answer!
    If the context Is empty, Please Say "The document provided doesn't contain the answer you're seeking for your question. Please consider rephrasing it or trying another approach."!

    The answer has to be formated using the markdown format!

    context: {context}

    question: {question}

    Use markdown Headings to add titles.

    answer:
    """

    messages.append(
        {
            "role": "system",
            "content": prompt,
        }
    )

    return manager.get_chat_completion_stream_with_messages(messages)


def filter(context, question, manager):
    prompt = f"""
    Does the following context "{context}" contain the answer for the question "{question}"?
    Answer only with "YES" or "NO"!

    answer:
    """
    filter_response = manager.get_chat_completion(prompt).strip()

    return (
        (filter_response == "YES")
        or (filter_response == "Yes")
        or (filter_response == "yes")
    )


def summarize(input, manager):
    prompt = f"""
    Summarize the following passage in detail

    passage: {input}

    summary:
    """

    return manager.get_chat_completion(prompt)


def suggest_questions(context, manager):
    prompt = f"""
    Generate an array of 10 questions suggestions about {context}.

    result sould be formatted as a python list
    suggestions: 
    """

    return manager.follow_instruction(prompt)

