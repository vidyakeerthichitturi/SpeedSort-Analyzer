from flask import Flask, render_template, request
import time
import random

app = Flask(__name__)

# Bubble Sort
def bubble_sort(arr):
    arr = arr.copy()
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Merge Sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

@app.route("/", methods=["GET", "POST"])
def home():

    numbers = ""
    bubble_output = ""
    merge_output = ""
    bubble_time = ""
    merge_time = ""
    winner = ""
    arr = []

    if request.method == "POST":

        action = request.form.get("action")

        # ---------------- GENERATE 100 ----------------
        if action == "generate100":
            arr = [random.randint(1, 1000) for _ in range(100)]
            numbers = ", ".join(map(str, arr))

        # ---------------- GENERATE 1000 ----------------
        elif action == "generate500":
            arr = [random.randint(1, 10000) for _ in range(500)]
            numbers = ", ".join(map(str, arr))

        # ---------------- ANALYZE ----------------
        elif action == "analyze":
            numbers = request.form.get("numbers", "")

            try:
                arr = [int(x) for x in numbers.replace(",", " ").split()]
            except:
                arr = []

        # ---------------- SORTING ----------------
        if action=="analyze" and arr:

            start = time.perf_counter()
            bubble_output = bubble_sort(arr)
            bubble_time = round((time.perf_counter() - start) * 1000, 5)

            start = time.perf_counter()
            merge_output = merge_sort(arr)
            merge_time = round((time.perf_counter() - start) * 1000, 5)

            if bubble_time < merge_time:
                winner = "🏆 Bubble Sort is Faster"
            elif merge_time < bubble_time:
                winner = "🏆 Merge Sort is Faster"
            else:
                winner = "⚖ Both Algorithms Took the Same Time"

    return render_template(
        "index.html",
        numbers=numbers,
        bubble_output=bubble_output,
        merge_output=merge_output,
        bubble_time=bubble_time,
        merge_time=merge_time,
        winner=winner
    )


if __name__ == "__main__":
    app.run(debug=True)



