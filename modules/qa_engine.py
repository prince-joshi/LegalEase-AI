from transformers import pipeline

def load_qa():
    """Load pre-trained question answering model (RoBERTa fine-tuned on SQuAD 2.0)"""
    qa_pipeline = pipeline(
        "question-answering",
        model="deepset/roberta-base-squad2"
    )
    return qa_pipeline

def answer_question(question, document_text, qa_pipeline):
    """Answer question based on document content using extractive QA"""
    if not question.strip():
        return "Please enter a question."

    if not document_text.strip():
        return "No document text available."

    try:
        result = qa_pipeline(
            question=question,
            context=document_text
        )

        answer = result["answer"].strip()

        if not answer:
            return "Answer not found in the document."

        return answer

    except Exception:
        return "Unable to generate answer."