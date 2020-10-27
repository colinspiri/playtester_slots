

def start_search(all_times, playtesters):
	playtester_order = list(playtesters.keys())
	print(playtester_order)
	valid = backtracking_search(all_times, playtesters, playtester_order)
	print("\n")
	if valid:
		print("SUCCESS!")
	else:
		print("FAILURE!")
	print("\n")
	return all_times


def backtracking_search(all_times, playtesters, playtester_order, p=0):
	# If p is out of range, completed search
	if(p >= len(playtester_order)):
		return True

	current_playtester = playtester_order[p]
	print("Current playtester = " + current_playtester + ", p = " + str(p))

	# Iterate through all possible times
	time_available = False
	for time in playtesters[current_playtester]:
		print("  Trying time " + time)
		valid_time = False

		# If time is valid, assign all variables
		if time_is_available(all_times, time):
			valid_time = True
			cohort_member = assign_cohort_member(all_times, time)
			all_times[time][cohort_member] = current_playtester
		
		# If time was picked, recurse
		if valid_time:
			print("  Picked " + time)
			valid = backtracking_search(all_times, playtesters, playtester_order, p + 1)
			# If recursing results in blockages, pick another time
			if not valid:
				# Unassign all variables
				print("Back to playtester = " + current_playtester + ", p = " + str(p))
				all_times[time][cohort_member] = "FREE"
				continue
			else:
				return True
	# If no time was found, return false
	if not time_available:
		print("  No time was found, backtracking...")
		return False


# Returns if the time has spots available
def time_is_available(all_times, time):
	return assign_cohort_member(all_times, time) != ""

# Given a time, return the next available cohort member
def assign_cohort_member(all_times, time):
	slots = all_times[time]
	for cohort_member, playtester in slots.items():
		if playtester == "FREE":
			return cohort_member
	return ""
