from flask import Flask, render_template, request
from datetime import timedelta, datetime
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/output', methods=["POST", "GET"])
def output():
    if request.method == 'POST':

        f = request.files['chosen_file']
        file = f.filename
        f.save(f.filename)

        if '.txt' not in file:
            return render_template('error.html',msg='Please select .txt file')


        else:
            x = open(f.filename, 'r')
            x = x.readlines()
            # print(x[0].lower())
            if 'time log:' not in x[0].lower():
                return render_template('error.html',msg='Time Log: is missing')
            else:
                start_time = []
                end_time = []
                c = 1

                for i in x:
                    a = i.strip().split(' ')
                    try:
                        index = a.index('-')
                        if index == 0:
                            # print('Error in line: ',c)
                            continue
                        else:
                            start_index = index - 1
                            end_index = index + 1
                            start_time.append(a[start_index])
                            end_time.append(a[end_index])
                    except:
                        if '-' in i:
                            ind = i.index('-')
                            end = i[ind+1:ind+8].strip()
                            start = i[ind-7:ind].strip()
                            start_time.append(start)
                            end_time.append(end)
                    c += 1

                def convert_time(x):
                    final_time = []
                    for i in x:
                        try:
                            s = time.strptime(i, '%I:%M%p')
                            fi = time.strftime('%H:%M', s)
                            final_time.append(fi)
                        except:
                            pass
                    return final_time


                s_24 = convert_time(start_time)
                e_24 = convert_time(end_time)


                c = []
                zipped_lists = zip(s_24, e_24)
                for i in zipped_lists:
                    #     print(i[1],i[0])
                    total = datetime.strptime(i[1], '%H:%M') - datetime.strptime(i[0], '%H:%M')
                    if total.days < 0:
                        total = timedelta(days=0, seconds=total.seconds)
                    c.append(total)

                #     print(total)
                cc = []
                for i in c:
                    c = str(i)
                    cc.append(c)

                totalSecs = 0
                for tm in cc:
                    timeParts = [int(s) for s in tm.split(':')]
                    totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60
                totalSecs, sec = divmod(totalSecs, 60)
                hr, min = divmod(totalSecs, 60)
                # print(hr,min)

        return render_template('output.html', Hours=hr, Minutes=min)


if __name__ == '__main__':
    app.run()

