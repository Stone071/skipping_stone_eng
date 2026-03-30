from flask import request, jsonify
import io

def calculate():
    print("Received request:", request.method, request.is_json)

    data = request.get_json()
    principal = float(data['principal'])
    eras = data['eras']

    time = [] # Time forms labels for our x axis ultimately
    year_index = 0 # year_index
    running_balance = [] # calculate the balances for each era
    previous_value = 0     # Need to initialize previous value up here
    current_balance = principal
    era_balances = []
    # balances where datapoints are [X,Y] tuples
    # and each element in the array is a set of these [X,Y] datapoints for
    # an era
    # [ balance:{[X1,Y1],[X2,Y2]} , balance:{[],[]} ]

    for era_num, era in enumerate(eras):
        # Grab parameters for this era.
        era_years = int(era['years'])
        era_rate = float(era['rate'])/100
        era_comp_freq = int(era['compound_freq'])
        era_deposit = float(era['deposit'])
        era_dep_freq = int(era['deposit_freq'])
        # We now always calculate on a monthly basis.
        num_points = era_years * 12

        # Go through the years in the era and calculate the balance.
        # We need to format the balance datapoints as [X, Y] tuples for chart.js.
        for i in range(0, num_points+1):
            # Initialize the new era
            if (i == 0):
                # Running balance is captured at the end of each year. Reset for each era.
                running_balance = []
                # for i == 0, there will always be a deposit, and never interest.
                # The transition year is gone over twice. Once in the previous era, where
                # the value is actually calculated, and once in the next era, where the value is
                # 'deposited' in, and no interest is calculated.
                deposit = principal if (era_num == 0) else (previous_value)
                rate = 0
                previous_value = 0
                current_balance = 0
                value_for_compounding = 0
            elif (i > 0):
                # Rate is 0 unless it's the right month to compound.
                if ((era_comp_freq == 1 and (i % 12 == 0)) or era_comp_freq == 12):
                    rate = (era_rate/12) if (era_comp_freq == 12) else (era_rate)
                else:
                    rate = 0
                # Deposit is 0 unless it's the right month to deposit
                if ((era_dep_freq == 1 and (i % 12 == 0)) or era_dep_freq == 12):
                    deposit = era_deposit
                else:
                    deposit = 0

            # Do the calc, update previous_value for the next calc.
            current_balance = previous_value + (value_for_compounding * (rate)) + deposit
            previous_value = current_balance
            # if you just compounded, save the value for the next time we compound.
            if ((era_comp_freq == 1 and (i % 12 == 0)) or era_comp_freq == 12):
                value_for_compounding = current_balance

            # Save the data in running_balance[] and time[]
            # if (i == 0):
            #     time.append(year_index)
            #     running_balance.append([year_index, current_balance])
            if (i % 12 == 0):
                running_balance.append([year_index, current_balance])
                if i != num_points:
                    time.append(year_index)
                    # Do not increment year at the very end of an era. The year must be
                    # The same at the beginning of the next era. Allow the next era to be
                    # the one to append the year to the labels
                    year_index += 1
                elif (era_num == (len(eras) - 1)):
                    # Allow the last era to append the last year.
                    time.append(year_index)

            #print("i:", i)
            #print("CURRENT_BAL:",current_balance)
            #print("TIME:", time)
            #print("RUNNING_BALANCE:",running_balance)


        # Save off the calculated balances for the era you just calculated
        era_balances.append({"balance": running_balance})

    final_value = round(current_balance, 2)
    total_gain = round(final_value - principal, 2)

    return jsonify({
        'final_value': final_value,
        'total_gain': total_gain,
        'time': time,
        'eras': era_balances
    })

# def download_csv():
#     global latest_csv_data
#     output = io.StringIO()
#     writer = csv.writer(output)
#     writer.writerows(latest_csv_data)
#     output.seek(0)
#     return send_file(
#         io.BytesIO(output.getvalue().encode()),
#         mimetype='text/csv',
#         as_attachment=True,
#         download_name='compound_interest.csv'
#     )