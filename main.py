from kaggle_environments import evaluate, make

def main_submit():
    env = make("halite", debug=True)

    env.run(["submission.py", "Random"])
    print("EXCELLENT SUBMISSION!" if env.toJSON()["statuses"] == ["DONE", "DONE"] else "MAYBE BAD SUBMISSION?")

    # Change mode from ipython -> html
    out = env.render(mode="html", width=800, height=600)
    # Write the output to a html file so we can open in a browser.
    f = open("halite.html", "w")
    f.write(out)
    f.close()

if __name__ == "__main__":
    main_submit()
