import json

def get_cohort_slots():
    data = get_json_as_object("cohort_slots.json")
    times = {
        "200": [],
        "215": [],
        "230": [],
        "245": [],
        "300": [],
        "315": [],
        "330": [],
        "345": []
    }
    for name, available_times in data.items():
        for available_time in available_times:
            times[str(available_time)].append(name)
    return times

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