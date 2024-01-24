import os
from semantic_router.encoders import CohereEncoder
from semantic_router import Route
from semantic_router import RouteLayer
from tabulate import tabulate

os.environ['COHERE_API_KEY'] = "sbSVmPosNgOfCJ96FQMGAoGDIiKyhLyj3bF9m0PN"

data_processing = Route(
    name="data_processing",
    utterances=[
        "process data and generate report",
        "analyze dataset for insights",
        "data cleaning and transformation",
    ],
)

file_management = Route(
    name="file_management",
    utterances=[
        "organize files in the project directory",
        "move files to archive",
        "rename documents based on date",
    ],
)

email_automation = Route(
    name="email_automation",
    utterances=[
        "send automated follow-up emails",
        "organize inbox using filters",
        "schedule email campaigns",
    ],
)

meeting_scheduling = Route(
    name="meeting_scheduling",
    utterances=[
        "schedule a team meeting for next week",
        "find available time slots for a conference call",
        "set up recurring team catch-ups",
    ],
)

task_routes = [data_processing, file_management, email_automation, meeting_scheduling]

encoder = CohereEncoder()

def print_semantic_router_info(route_layer):
    print(f"{route_layer.encoder.type=}")
    print(f"{route_layer.encoder.name=}")
    print(f"{route_layer.routes=}")

def augment_user_query(user_query, route_name):
    prompt_templates = {
        "data_processing": "Process the provided dataset to generate detailed insights and reports. Utilize data cleaning and transformation techniques.",
        "file_management": "Organize and manage files in the project directory. Move files to the archive and rename documents based on the date.",
        "email_automation": "Automate the process of sending follow-up emails. Organize the inbox using filters and schedule email campaigns.",
        "meeting_scheduling": "Schedule team meetings for the upcoming week. Find available time slots for conference calls and set up recurring team catch-ups.",
    }

    if route_name in prompt_templates:
        augmented_query = f"{user_query}\n\nPrompt: {prompt_templates[route_name]}"
        return augmented_query
    else:
        return user_query

rl = RouteLayer(encoder=encoder, routes=task_routes)

print_semantic_router_info(rl)

queries = [
    "process data and generate report",
    "organize files in the project directory",
    "send automated follow-up emails",
    "schedule a team meeting for next week",
    "analyze sentiment in llama-related articles",
]

table_data = []

for query in queries:
    route_name = rl(query).name
    augmented_query = augment_user_query(query, route_name)
    table_data.append([query, augmented_query])

headers = ["User Query", "Augmented Query"]
print(tabulate(table_data, headers, tablefmt="grid"))
