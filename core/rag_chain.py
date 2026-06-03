def run_qa(qa_chain, query: str, lang: str) -> dict:
    full_query = f"Answer in {lang}. {query}"
    return qa_chain.invoke({"query": full_query})