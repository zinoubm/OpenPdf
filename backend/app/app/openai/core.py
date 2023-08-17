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
