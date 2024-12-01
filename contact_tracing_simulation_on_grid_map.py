import numpy as np
import matplotlib.pyplot as plt

class ContactTracer:
    def __init__(self):
        self.contact = []
    """
    def rolling_prox_id(self, base_id, time_interval):
        # Simulate the rolling prox_id as a coordinate
        return base_id[0] + np.random.normal(0, 0.1), base_id[1] + np.random.normal(0, 0.1)

    def doContactTracing(self, diagnosisKeys):
        contact_match = []  # Stores a list of possible contacts which occurred with Covid-19 infected individual. A tuple of (DayNumber, TimeInterval, Matching Prox ID).
        for dk in diagnosisKeys:
            for timeInterval in range(0, 144):  # each interval is equal to 10 minutes of time.
                prox_id = self.rolling_prox_id(dk[1], timeInterval)
                for c in self.contact:
                    if dk[0] == c[0] and prox_id == c[1]:  # If day and prox ID matches with contact list.
                        contact_match.append((dk[0], timeInterval, prox_id))
        return contact_match
    """
    
# Generate random trails for Bob and Alice
np.random.seed(42)  # For reproducibility

num_points = 1000  # Number of points (time intervals). If 10 mins per snapshot, it will be 144 in a day

# Bob's trail
bob_trail = np.cumsum(np.random.randn(num_points, 2) * 0.1, axis=0)

# Alice's trail
alice_trail = np.cumsum(np.random.randn(num_points, 2) * 0.1, axis=0)

# Initialize ContactTracer
tracer = ContactTracer()

# Simulate contacts (Bob and Alice cross paths randomly)
for i in range(num_points):
    if np.random.rand() < 0.05:  # 5% chance they are at the same place at the same time
        tracer.contact.append((0, bob_trail[i]))
    else:
        tracer.contact.append((1, alice_trail[i]))

# Plot the trails
plt.figure(figsize=(10, 6))
plt.plot(bob_trail[:, 0], bob_trail[:, 1], label='Bob', color='blue', alpha=0.7)
plt.plot(alice_trail[:, 0], alice_trail[:, 1], label='Alice', color='red', alpha=0.7)
plt.scatter(bob_trail[:, 0], bob_trail[:, 1], color='blue', alpha=0.7)
plt.scatter(alice_trail[:, 0], alice_trail[:, 1], color='red', alpha=0.7)

plt.title('Random Trails of Bob and Alice')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend()
plt.grid(True)
plt.show()

