import pickle
import dill
import cloudpickle

from timy import timer

def invert_dict(dict_: dict):
    new_dict = dict()

    for value in dict_.values():
        if(not isinstance(value, list)):
            emsg = 'All values must be lists!'
            raise ValueError(emsg)

    for key, value in dict_.items():
        for el in value:
            new_dict_key = list(new_dict.keys())
            if(el in new_dict_key):
                new_dict[el].append(key)
            else:
                new_dict[el] = [key]

    return new_dict

def flatten_list(lst : list):
    new_lst = []
    
    for el in lst:
        if(isinstance(el, list)):
            new_lst+=flatten_list(el)
        else:
            new_lst.append(el)
    
    return new_lst

def sum_dicts(dict_list):
    result = {}
    for d in dict_list:
        for key, value in d.items():
            if key not in result:
                result[key] = value
            else:
                result[key] += value
    return result

@timer()
def load_pickle(pkl_filepath: str) -> None:
    with open(pkl_filepath, 'rb') as f:
        return pickle.load(f)

@timer()
def dump_pickle(
    dump_file: any,
    pkl_filepath: str
) -> None:    
    # Dump training data to pickle
    with open(pkl_filepath, 'wb') as f:
        pickle.dump(dump_file, f)


@timer()
def load_dill(dill_filepath: str) -> None:
    with open(dill_filepath, 'rb') as f:
        return dill.load(f)

@timer()
def dump_dill(
    dump_file: any,
    dill_filepath: str
) -> None:    
    # Dump training data to dill
    with open(dill_filepath, 'wb') as f:
        dill.dump(dump_file, f)

@timer()
def load_cloudpickle(pkl_filepath: str) -> None:
    with open(pkl_filepath, 'rb') as f:
        return cloudpickle.load(f)

@timer()
def dump_cloudpickle(
    dump_file: any,
    pkl_filepath: str
) -> None:    
    # Dump training data to cloudpickle
    with open(pkl_filepath, 'wb') as f:
        cloudpickle.dump(dump_file, f)
