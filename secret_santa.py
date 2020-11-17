from collections import defaultdict
import random
import smtplib
import ssl
import sys
import time

### CONFIG ###
# Instructions: Follow the examples, replacing the reindeer with your friends!

ORGANIZER_NAME = "Rudolph"
ORGANIZER_EMAIL_ADDRESS = "rudolph@anitejb.dev"
GROUP_NAME = "North Pole Neighbors"
GROUP_INFO = {
    "Dasher": "dasher@anitejb.dev",
    "Dancer": "dancer@anitejb.dev",
    "Prancer": "prancer@anitejb.dev",
    "Vixen": "vixen@anitejb.dev",
    "Comet": "comet@anitejb.dev",
    "Cupid": "cupid@anitejb.dev",
    "Donner": "donner@anitejb.dev",
    "Blitzen": "blitzen@anitejb.dev",
    "Rudolph": "rudolph@anitejb.dev", # Don't forget to include yourself!
}

# NAUGHTY_LISTS is where you define any restrictions for people that should not be paired together
# If you do not have any restrictions, delete the example and uncomment the following line
# NAUGHTY_LISTS = dict()
NAUGHTY_LISTS = {
    "Dasher": ["Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Donner", "Blitzen"],
    "Rudolph": ["Dancer", "Vixen"],
    "Prancer": ["Vixen"],
}

### END CONFIG ###


ORGANIZER_EMAIL_PASSWORD = input(f"Enter password for {ORGANIZER_EMAIL_ADDRESS}: ")
NAUGHTY_LISTS = defaultdict(list, NAUGHTY_LISTS)
NICE_LISTS = defaultdict(list)
MATCHES = dict()
TIMEOUT = 10


def add_backward_edges():
    for name in GROUP_INFO:
        for bad_match in NAUGHTY_LISTS[name]:
            if name not in NAUGHTY_LISTS[bad_match]:
                NAUGHTY_LISTS[bad_match].append(name)


def create_nice_lists():
    all_names = set(GROUP_INFO.keys())
    for name in NAUGHTY_LISTS:
        NICE_LISTS[name] = list(all_names - set(NAUGHTY_LISTS[name] + [name]))
        if not NICE_LISTS[name]:
            print(
                "Current naughty list makes it impossible! Try loosening up some of those restrictions :)"
            )
            sys.exit()


def matchmaker(start_time):
    givers = list(GROUP_INFO.keys())
    random.shuffle(givers)
    receivers = set(givers)

    for giver in givers:
        nice_list = NICE_LISTS[giver]
        random.shuffle(nice_list)
        for receiver in nice_list:
            if receiver in receivers:
                MATCHES[giver] = receiver
                receivers.remove(receiver)
                break
        else:
            if time.time() - start_time < TIMEOUT:
                MATCHES.clear()
                return matchmaker(start_time)

            print(f"Secret Santa timed out after {TIMEOUT} seconds.")
            sys.exit()


def send_emails():
    smtp_server = "smtp.gmail.com"
    port = 587  # starttls

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(ORGANIZER_EMAIL_ADDRESS, ORGANIZER_EMAIL_PASSWORD)

            for receiver_name, receiver_email in GROUP_INFO.items():
                message = (
                    f"Subject: Secret Santa for {GROUP_NAME}!"
                    f"\nTo: {receiver_name} <{receiver_email}>"
                    f"\nFrom: Santa's Helper {ORGANIZER_NAME} <{ORGANIZER_EMAIL_ADDRESS}>"
                    f"\n\nHi {receiver_name}!\n\nYou've been assigned to: {MATCHES[receiver_name]}.\n\nHappy Holidays!"
                )

                try:
                    server.sendmail(ORGANIZER_EMAIL_ADDRESS, receiver_email, message)
                    print(
                        f"Successfully sent an email to {receiver_name} ({receiver_email})!"
                    )
                except Exception as e:
                    print(
                        f"Failed to send an email to {receiver_name} ({receiver_email}) :(\nException: {e}"
                    )

    except Exception as e:
        print(f"Secret Santa failed :(\nException: {e}")


if __name__ == "__main__":
    add_backward_edges()
    create_nice_lists()
    matchmaker(time.time())
    send_emails()
