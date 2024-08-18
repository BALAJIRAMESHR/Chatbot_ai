from django.shortcuts import render
from django.http import JsonResponse
import json
from difflib import get_close_matches


def load_knowledge_base(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def save_knowledge_base(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question, createdata):
    for q in createdata["questions"]:
        if isinstance(q["question"], list):
            matches = get_close_matches(user_question, q["question"], n=1)
            if matches:
                return matches[0]
        else:
            if q["question"] == user_question:
                return q["question"]
    return None


def get_answer_for_question(question, createdata):
    for q in createdata["questions"]:
        if isinstance(q["question"], list) and question in q["question"]:
            return q["answer"]
        elif q["question"] == question:
            return q["answer"]
    return None


def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        createdata = load_knowledge_base("createdata.json")

        best_match = find_best_match(user_input, createdata)

        if best_match:
            answer = get_answer_for_question(best_match, createdata)
            response = {"answer": answer}
        else:
            response = {"answer": "I don't know"}
            new_answer = request.POST.get("new_answer", "")
            if new_answer and new_answer.lower() != "skip":
                createdata["questions"].append(
                    {"question": [user_input], "answer": new_answer}
                )
                save_knowledge_base("createdata.json", createdata)

        return JsonResponse(response)
    else:
        return render(request, "chat.html")
