

def format_params(params):
    # params_list = list(row.split(":") for row in str(params).split(","))
    param_args = dict()
    for row in list(row.split(":") for row in str(params).split(",")):
        param_args[row[0]] = row[1]
    # print(param_args)
    return param_args