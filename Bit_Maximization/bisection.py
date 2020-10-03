from bit_maximization import OneMaxProblem, TrappedOneMaxProblem


def run_multiple_times(times, Problem, mode):
	evals = 0
	for _ in range(times):
		result = True
		x = 0
		if mode['cross-over'] == "single_point":
			x, result = Problem.maximize_single_point()
		elif mode['cross-over'] == "uniform":
			x, result = Problem.maximize_uniform()
		if result == False:
			return 0, False
		evals += x
	return evals/times, True


def get_MRPS_upper_bound(problem_size, random_seed, mode):
	N_upper = 4
	Problem = None
	
	if mode['problem'] == "normal":
		Problem = OneMaxProblem(problem_size, N_upper, random_seed)
	elif mode['problem'] == "trap":
		Problem = TrappedOneMaxProblem(problem_size, N_upper, random_seed)

	evals, success = run_multiple_times(10, Problem, mode)
	while (not success and N_upper < 8192):

		N_upper = N_upper * 2
		if mode['problem'] == "normal":
			Problem = OneMaxProblem(problem_size, N_upper, random_seed)
		elif mode['problem'] == "trap":
			Problem = TrappedOneMaxProblem(problem_size, N_upper, random_seed)
		evals, success = run_multiple_times(10, Problem, mode)
		print(f'success: {success}  -  N_upper: {N_upper}')
	return N_upper, evals, success

def find_MRPS(N_upper, evals_upper, problem_size, random_seed, mode):
	N_lower = N_upper // 2
	evals = evals_upper
	while (N_upper - N_lower)/N_upper > 0.1:
		N = (N_upper + N_lower) // 2
		Problem = None
		if mode['problem'] == "normal":
			Problem = OneMaxProblem(problem_size, N, random_seed)
		elif mode['problem'] == "trap":
			Problem = TrappedOneMaxProblem(problem_size, N, random_seed)
		x, success = run_multiple_times(10, Problem, mode)

		print(f'N_upper: {N_upper} - N_lower: {N_lower} - success: {success} - x: {x}')
		if success:
			N_upper = N
		else:
			N_lower = N
		
		if (N_upper - N_lower) <= 2:
			return evals, N_upper
		if success:
			evals = x
	return evals, N_upper

def bisection(problem_size, random_seed, mode):
	N_upper, evals_upper, success = get_MRPS_upper_bound(problem_size, random_seed, mode)
	if not success:
		return 0, 0, False
	evals, MRPS = find_MRPS(N_upper, evals_upper, problem_size, random_seed, mode)
	return evals, MRPS, True
