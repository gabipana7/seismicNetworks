def query(region):

    # VRANCEA
    if region=='vrancea':
        #year = input('Input year from which you want visualization (recommended: 1976) : ')
        year = '1976'
        dateandtime = year + '-01-01 00:00:00'
        condition=(f"SELECT * FROM romania WHERE datetime >='{dateandtime}'"
            f" AND latitude>=45.2 AND latitude<=46 AND longitude>=26" 
            f" AND longitude<=27 AND depth>=50 AND depth<=200")
        
    # ROMANIA
    if region=='romania':
        #year = input('Input year from which you want visualization (recommended: 1976) : ')
        year = '1976'
        dateandtime = year + '-01-01 00:00:00'
        condition=f"SELECT * FROM romania WHERE datetime>='{dateandtime}'"

    # CALIFORNIA
    if region=='california':
        #year = input('Input year from which you want visualization (recommended: 1984) : ')
        year = '1984'
        dateandtime = year + '-01-01 00:00:00'
        condition=(f"SELECT * FROM california WHERE datetime>='{dateandtime}'"
                    f" AND magtype IN ('l','w')")

    # ITALY
    if region=='italy':
        #year = input('Input year from which you want visualization (recommended: 1986) : ')
        year = '1986'
        dateandtime = year + '-01-01 00:00:00'
        condition=f"SELECT * FROM italy WHERE datetime>='{dateandtime}' AND depth>=0"

    # JAPAN
    if region=='japan':
        #year = input('Input year from which you want visualization (recommended: 1992) : ')
        year = '1992'
        dateandtime = year + '-01-01 00:00:00'
        condition=(f"SELECT * FROM japan WHERE datetime>='{dateandtime}'"
                    f" AND latitude>0 AND longitude>0 AND depth>0"
                    f" AND magtype IN ('V','v','D','d','W')")

    return condition