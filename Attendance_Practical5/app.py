from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def attendance():

    results = []

    if request.method == "POST":

        for i in range(10):

            roll_number = request.form.get(f"roll_number_{i}")
            name = request.form.get(f"name_{i}")
            total_classes = request.form.get(f"total_classes_{i}")
            attended_classes = request.form.get(f"attended_classes_{i}")

            if roll_number and name and total_classes and attended_classes:

                total_classes = int(total_classes)
                attended_classes = int(attended_classes)

                attendance = (attended_classes / total_classes) * 100

                if attendance >=  90:
                     status = "Eligible"
                     message = "🏆 Outstanding! Your attendance is excellent. You are definitely ready for the examination!"

                elif attendance >= 80:
                        status = "Eligible"
                        message = "🌟 Excellent! You have maintained great attendance and are eligible for the examination."

                elif attendance >= 75:
                         status = "Eligible"
                         message = "🎉 Congratulations! You meet the 75% requirement and are eligible for the examination."

                else:
                        status = "Not Eligible"
                        message = "😭 Oops! Your attendance is below 75%. Please attend more classes next time."

                results.append({
                    "roll_number": roll_number,
                    "name": name,
                    "attendance": round(attendance, 2),
                    "status": status,
                    "message": message
                })

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)