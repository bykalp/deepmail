emails = open("crawlables.txt","r").read().split("\n")
total = list(set(emails))
print len(total)
with open("final_mails.txt","a") as finalmail:
	for each in total:
		finalmail.write(each+"\n")
