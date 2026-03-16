"""
evaluate.py
-----------
Runs the golden dataset through the RAG pipeline and
scores each answer for correctness and refusal accuracy.
No external API needed — we score manually with clear criteria.
"""

import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline import answer


def evaluate_golden_dataset(dataset_path: str = "evaluation/golden_dataset.json"):

    with open(dataset_path) as f:
        dataset = json.load(f)

    results = []
    correct = 0
    refusals_correct = 0
    refusals_total   = sum(1 for q in dataset if not q['answerable'])
    answerable_total = sum(1 for q in dataset if q['answerable'])

    print(f"Running evaluation on {len(dataset)} questions...")
    print("=" * 70)

    for i, item in enumerate(dataset, 1):
        question    = item['question']
        ground_truth = item['ground_truth'].lower()
        answerable  = item['answerable']

        result = answer(question, k=5)
        response = result['answer'].lower()

        # Score
        if not answerable:
            # Should say not available
            refused = "not available" in response or "not contain" in response
            score   = 1 if refused else 0
            status  = "CORRECT REFUSAL" if refused else "HALLUCINATED"
            refusals_correct += score
        else:
            # Check if key terms from ground truth appear in response
            gt_words = [w for w in ground_truth.split() if len(w) > 4]
            matches  = sum(1 for w in gt_words if w in response)
            score    = 1 if matches >= max(2, len(gt_words) // 3) else 0
            status   = "CORRECT" if score else "MISSED"
            correct += score

        results.append({
            'question'    : question,
            'answerable'  : answerable,
            'status'      : status,
            'score'       : score,
            'answer_preview': result['answer'][:120].replace('\n', ' '),
        })

        print(f"[{i:02d}] {status:<18} {question[:55]}")

    # Summary
    print("\n" + "=" * 70)
    print(f"EVALUATION SUMMARY")
    print(f"=" * 70)
    print(f"Answerable questions : {correct}/{answerable_total} correct")
    print(f"Unanswerable (refusals): {refusals_correct}/{refusals_total} correct")
    total_score = (correct + refusals_correct) / len(dataset)
    print(f"Overall accuracy     : {total_score:.1%}  ({correct + refusals_correct}/{len(dataset)})")
    print(f"=" * 70)

    # Save results
    output_path = "evaluation/results.json"
    with open(output_path, 'w') as f:
        json.dump({
            'total'              : len(dataset),
            'answerable_correct' : correct,
            'answerable_total'   : answerable_total,
            'refusals_correct'   : refusals_correct,
            'refusals_total'     : refusals_total,
            'overall_accuracy'   : round(total_score, 3),
            'results'            : results,
        }, f, indent=2)

    print(f"\nDetailed results saved to {output_path}")
    return total_score


if __name__ == "__main__":
    evaluate_golden_dataset()