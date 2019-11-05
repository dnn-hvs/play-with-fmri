import os


def create_god_dataset(address):
    god_dataset = {
        'mask_addresses': get_mask_addresses(os.path.join(address, 'sourcedata')),
        'T1_T2_masks': get_T1T2_mask_addresses(address),
        'func_addresses': get_func_addresses(address),
        'event_addresses': get_event_addresses(address)
    }
    return god_dataset


def get_mask_addresses(address="../data/sourcedata/"):
    mask_addresses = {}
    for subdir, dirs, files in os.walk(address):
        if len(files) > 1:  # > 1 to avoid adding sourcedata folder.
            mask_addresses[subdir.split(
                '/')[-2]] = [os.path.join(subdir, file_name) for file_name in files]
    print("Mask Addresses", mask_addresses.keys())
    return mask_addresses


def get_T1T2_mask_addresses(address="../data"):
    T2_mask_addrs = {}
    for subdir, dirs, files in os.walk(address):
        if "sourcedata" in subdir:
            continue
        if len(files) == 1:
            sub_name = subdir.split('/')[-3]
            if sub_name == "data" or sub_name == "..":
                continue
            if sub_name not in T2_mask_addrs.keys():
                T2_mask_addrs[sub_name] = [os.path.join(subdir, files[0])]
            else:
                T2_mask_addrs[sub_name].append(os.path.join(subdir, files[0]))
    print("T1T2 Addresses", T2_mask_addrs.keys())

    return T2_mask_addrs


def get_func_addresses(address="../data"):
    return func_or_event_addr("func", address)


def get_event_addresses(address="../data"):
    return func_or_event_addr("event", address)


def func_or_event_addr(val, addr):
    addresses = {}
    for subdir, dirs, files in os.walk(addr):
        if "func" in subdir and len(files) > 0:
            sub_name = subdir.split('/')[-3]
            if val == "func":
                paths = [os.path.join(subdir, file_name)
                         for file_name in files if "nii.gz" in file_name]
            else:
                paths = [os.path.join(subdir, file_name)
                         for file_name in files if "events.tsv" in file_name]

            if sub_name not in addresses.keys():
                addresses[sub_name] = paths
            else:
                addresses[sub_name].extend(paths)
    print("func Addresses", addresses.keys())
    return addresses


def get_full_filename(god, file_type, subj_name, file_name):
    return [filename for filename in god[file_type][subj_name] if file_name in filename]
