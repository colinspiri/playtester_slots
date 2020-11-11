import json

def get_cohort_slots():
    data = get_json_as_object("cohort_slots.json")
    times = {
        "200": [],
        "230": [],
        "300": [],
        "330": []
    }
    for name, available_times in data.items():
        for available_time in available_times:
            times[str(available_time)].append(name)
    return times

def get_preferred_matches():
    data = get_json_as_object("preferred_matches.json")
    # Prune people that haven't signed up
    playtester_slots = get_playtester_slots()
    pruned_data = {}
    for cohort_member, list_of_people in data.items():
        pruned_list = []
        for playtester in list_of_people:
            if playtester in playtester_slots:
                pruned_list.append(playtester)
        if len(pruned_list) > 0:
            pruned_data[cohort_member] = pruned_list
    return pruned_data

def get_playtester_slots():
    data = get_json_as_object("playtester_slots.json")
    for name, times in data.items():
        times_str = []
        for time_num in times:
            times_str.append(str(time_num))
        data[name] = times_str
    return data


def get_json_as_object(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        return data

def store_final_slots(data):
    # Prune all the "FREE" spots out of the final json
    for time, slots in data.items():
        pruned_slots = {}
        for cohort_member, playtester in slots.items():
            if playtester != "FREE":
                pruned_slots[cohort_member] = playtester
        data[time] = pruned_slots
    # Then store in json file
    store_as_json_file(data, "final_slots.json")

def store_as_json_file(data, filename):
    json_object = json.dumps(data, indent=2)
    with open(filename, 'w') as file:
        file.write(json_object)