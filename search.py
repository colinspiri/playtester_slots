import copy
import random

def start_search(all_times, playtesters, preferred_matches):
	# Get order of playtesters in a list
	playtester_order = list(playtesters.keys())
	# Try to assign preferred matches
	valid = False
	for cohort_member, pref_playtesters in preferred_matches.items():
		print("Looking for a match for " + cohort_member)
		found_match = False
		for playtester in pref_playtesters:
			if found_match:
				break
			print("  with " + playtester)
			for time, slot in all_times.items():
				if found_match:
					break
				print("    at " + time)
				if cohort_member in all_times[time].keys():
					if all_times[time][cohort_member] == "FREE":
						# print("     Assigning to " + time)
						all_times[time][cohort_member] = playtester
						all_times_copy = copy.deepcopy(all_times)
						valid = backtracking_search(all_times_copy, playtesters, playtester_order)
						if valid:
							found_match = True
						else:
							all_times[time][cohort_member] = "FREE"
						break
				else:
					continue
	# Start backtracking search
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

	if p == 0:
		print("backtracking_search()...")

	current_playtester = playtester_order[p]
	print("Current playtester = " + current_playtester + ", p = " + str(p))

	# Iterate through all possible times
	time_available = False
	shuffled_times = playtesters[current_playtester]
	random.shuffle(shuffled_times)
	for time in shuffled_times:
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
	# Add available members to a set
	available_cohort_members = []
	for cohort_member, playtester in slots.items():
		if playtester == "FREE":
			available_cohort_members.append(cohort_member)
	if len(available_cohort_members) == 0:
		return ""
	# Pick the one with the least playtests done so far
	chosen_member = available_cohort_members[0]
	# print("      " + str(get_frequency_of(all_times, chosen_member)) + " is the lowest ")
	for member in available_cohort_members:
		if get_frequency_of(all_times, member) < get_frequency_of(all_times, chosen_member):
			chosen_member = member
			# print("      " + chosen_member + " is new member with " + str(get_frequency_of(all_times, chosen_member)))
	return chosen_member

# Get how many playtests they're scheduled for
def get_frequency_of(all_times, name):
	frequency = {}
	for time, slots in all_times.items():
		for cohort_member, playtester in slots.items():
			if playtester == "FREE":
				continue
			if cohort_member in frequency:
				frequency[cohort_member] += 1
			else:
				frequency[cohort_member] = 1
	if name not in frequency:
		return 0
	else:
		return frequency[name]