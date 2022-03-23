def inp_valid(x):
    try:
        x=int(x)
        if x<=1 or x>=5:
            raise TypeError("Please key in an integer from 1 to 5.")
        
    except ValueError:
        print("Please key in an integer from 1 to 5.")
    except TypeError as err:
        print(err)
    return x