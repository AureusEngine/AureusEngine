
from predict_2mat import predict_2mat_distribution

def run_sample_tests():
    test_cases = [("Y", "P"), ("C", "C"), ("E", "X"), ("X", "P")]
    for mat1, mat2 in test_cases:
        result = predict_2mat_distribution(mat1, mat2)
        print(f"\n{mat1}{mat2} Prediction:")
        for tier, pct in result.items():
            print(f"  {tier}: {pct:.2f}%")

if __name__ == "__main__":
    run_sample_tests()
