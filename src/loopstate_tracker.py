import time
import random
import logging

def simulate_drift_check():
    return {
        "emotional_vector": random.choice(["stable", "minor_wave", "spike"]),
        "ethics_alignment": round(random.uniform(0.78, 0.99), 3),
        "drift_index": round(random.uniform(0.01, 0.25), 3)
    }

def main():
    logging.basicConfig(level=logging.INFO)
    while True:
        status = simulate_drift_check()
        logging.info(f"Vector: {status['emotional_vector']}, Alignment: {status['ethics_alignment']}, Drift: {status['drift_index']}")
        time.sleep(3)

if __name__ == "__main__":
    main()
