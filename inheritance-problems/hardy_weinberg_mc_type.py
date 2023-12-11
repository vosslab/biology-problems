import random


choices = [
	"p &mdash; Frequency of the dominant allele",
	"q &mdash; Frequency of the recessive allele",
	"p&sup2; &mdash; Frequency of homozygous dominant individuals",
	"q&sup2; &mdash; Frequency of homozygous recessive individuals",
	"2pq &mdash; Frequency of heterozygous individuals",
	"p&sup2; + 2pq &mdash; Frequency of individuals with the dominant phenotype",
	"2pq + q&sup2; &mdash; Frequency of individuals that are not homozygous dominant"
]



In the depths of the Amazon rainforest, a team of scientists collected a sample of 70 butterflies from a unique species known for its striking color variation. They observed that 49 of these butterflies exhibited the bright color trait, which is known to be dominant.

def generate_p_question():
	pass

#=========================
def make_interesting_fraction(n, d=10000):
	#assume out of 10000
	# given numerator, n and denominator, d
	n = int(n)
	gcd = math.gcd(n, d)
	numerator = n // gcd
	denominator = d // gcd
	if denominator <= 100:
		factor = random.choice([7, 11, 13, 17])
		numerator *= factor
		denominator *= factor
	elif denominator <= 400:
		factor = random.choice([3, 7])
		numerator *= factor
		denominator *= factor
	if (numerator*1e4/denominator - n*1e4/d) > 0.1:
		print("something went wrong")
		sys.exit(1)
	return numerator, denominator

#=========================
def get_values(p=None):
	if p is None:
		p = get_good_p()
	q = round(1-p, 2)
	#hw
	p2 = round(p**2, 4)
	q2 = round(q**2, 4)
	twopq = round(2*p*q, 4)
	total_sum = p2 + twopq + q2
	if abs(total_sum - 1) > 1e-6:
		raise ValueError
	return p, q, p2, twopq, q2

#=========================
def get_good_p():
	max_p = 0.99
	min_p = 0.4
	r = random.random()
	r *= (max_p-min_p)
	r += min_p
	#alleles
	p = round(r, 2)
	return p

#=========================
def generate_hw_questions(num_questions):
	questions = []
	for _ in range(num_questions):
		p = get_good_p()
		question_type = random.choice(["type2a", "type2b"])
		if question_type == "type2a":
			question = makeType2aQuestion(p)
		else:
			question = makeType2bQuestion(p)
		questions.append(question)
	return questions

# Example usage
num_questions = 5
hw_questions = generate_hw_questions(num_questions)
for q in hw_questions:
	print(q)


def generate_hw_problem():
	variables = ["p", "q", "p^2", "2pq", "q^2", "p^2 + 2pq", "2pq + q^2"]
	given_var = random.choice(variables)
	answer_var = random.choice([v for v in variables if v != given_var])

	# Generating a random value for the given variable
	# Ensure biological plausibility (e.g., 0 < p, q < 1)
	given_value = round(random.uniform(0.01, 0.99), 2)
	if given_var in ["p^2", "q^2"]:
		given_value = round(given_value ** 2, 4)
	elif given_var == "2pq":
		q_val = round(random.uniform(0.01, 0.99), 2)
		given_value = round(2 * given_value * q_val, 4)

	problem_statement = f"Given {given_var} = {given_value}, what is {answer_var}?"

	# Here you would include logic to calculate the answer based on given_var and answer_var
	# ...

	return problem_statement

# Example usage
for _ in range(5):
	print(generate_hw_problem())
