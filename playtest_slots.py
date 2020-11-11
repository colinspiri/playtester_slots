import json_loader as loader
import search

# Get input data from files
cohort_slots = loader.get_cohort_slots()
playtesters = loader.get_playtester_slots()
preferred_matches = loader.get_preferred_matches()

# Initialize data
all_times = {
	"200": {},
	"230": {},
	"300": {},
	"330": {}
}
for time, slots in all_times.items():
	cohort_members = cohort_slots[time]
	for member in cohort_members:
		slots[member] = "FREE"

# Start search
search.start_search(all_times, playtesters, preferred_matches)

# Save all_times to json file
loader.store_final_slots(all_times)