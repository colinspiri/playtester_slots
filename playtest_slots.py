import json_loader as loader
import search

# Get input data from files
cohort_slots = loader.get_cohort_slots()
playtesters = loader.get_playtester_slots()

# Initialize data
all_times = {
	"200": {},
	"215": {},
	"230": {},
	"245": {},
	"300": {},
	"315": {},
	"330": {},
	"345": {}
}
for time, slots in all_times.items():
	cohort_members = cohort_slots[time]
	for member in cohort_members:
		slots[member] = "FREE"

# Start search
search.start_search(all_times, playtesters)

# Save all_times to json file
loader.store_final_slots(all_times)