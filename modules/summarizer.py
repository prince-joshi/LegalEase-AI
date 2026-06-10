from transformers import pipeline

def load_summarizer():
    """Load BART-large-CNN model for abstractive text summarization"""
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn"
    )
    return summarizer

def create_summary(text, summarizer):
    """Summarize a single text chunk with dynamic length"""
    text = text.strip()
    if not text or len(text) < 50:
        return text if text else "Document content is too short for summarization."
    
    word_count = len(text.split())
    
    if word_count < 50:
        return text
    
    # Dynamic length: proportional to input but capped
    max_len = min(400, max(150, word_count // 2))
    min_len = min(100, max(50, word_count // 4))
    
    try:
        summary = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            truncation=True
        )
        
        if summary and len(summary) > 0 and 'summary_text' in summary[0]:
            return summary[0]["summary_text"]
        else:
            return text[:300] + "..." if len(text) > 300 else text
            
    except Exception:
        return text[:400] + "..." if len(text) > 400 else text

def generate_summary(text, summarizer):
    """Generate summary with chunking for long documents"""
    if not text or not text.strip():
        return "No text available for summarization."

    # Normalize whitespace
    text = ' '.join(text.split())
    words = text.split()
    
    # Short documents: summarize directly
    if len(words) < 100:
        return create_summary(text, summarizer)

    # Long documents: chunk with overlap
    chunk_size = 400
    overlap = 50
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.strip()) > 50:
            chunks.append(chunk)
        
        # Limit to 3 chunks for performance
        if len(chunks) >= 3:
            break

    if not chunks:
        return text[:400] + "..." if len(text) > 400 else text

    # Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        if len(chunk.strip()) > 50:
            summary = create_summary(chunk, summarizer)
            if summary and len(summary) > 10:
                chunk_summaries.append(summary)

    if not chunk_summaries:
        return text[:400] + "..." if len(text) > 400 else text

    combined_summary = " ".join(chunk_summaries)
    
    # Re-summarize if still too long
    if len(combined_summary.split()) > 300:
        try:
            final_summary = create_summary(combined_summary, summarizer)
            return final_summary
        except Exception:
            return combined_summary[:500] + "..."
    
    return combined_summary