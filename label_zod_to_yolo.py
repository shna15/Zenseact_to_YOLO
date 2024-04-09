import json
import os

def calculate_normalized_center(geometry, image_width, image_height):
    # Calculate the center coordinates of the bounding box
    x_center = (geometry[0][0] + geometry[1][0] + geometry[2][0] + geometry[3][0]) / 4
    y_center = (geometry[0][1] + geometry[1][1] + geometry[2][1] + geometry[3][1]) / 4

    # Normalize the center coordinates and round to 5 decimal places
    normalized_x_center = round(x_center / image_width, 5)
    normalized_y_center = round(y_center / image_height, 5)

    return normalized_x_center, normalized_y_center


def convert_to_yolo_format(data, image_width, image_height):
    yolo_labels = []
    class_mapping = {}

    # Hardcoded class mappings
    class_mappings = {
        "Unclear": None, #class id -1
        "NotListed": 0,
        "Indication_CameraSurveillance": 1,
        "Mandatory_PassOnEitherSide": 2,
        "Mandatory_PassOnThisSideLeft": 3,
        "Mandatory_PassOnThisSideRight": 4,
        "Mandatory_ProceedStraight": 5,
        "Mandatory_ProceedStraightOrTurnRight": 6,
        "Mandatory_ProceedStraightOrTurnLeft": 7,
        "Mandatory_Roundabout": 8,
        "Mandatory_TurnAhead": 9,
        "Mandatory_TurnLeft": 10,
        "Mandatory_TurnLeftAhead": 11,
        "Mandatory_TurnRight": 12,
        "Mandatory_TurnRightAhead": 13,
        "Priority_GiveWayOncoming": 14,
        "Priority_GiveWay": 15,
        "Priority_PriorityRoadBegin": 16,
        "Priority_PriorityRoadEnd": 17,
        "Priority_PrioOverOncoming": 18,
        "Priority_Stop": 19,
        "Prohibitory_MaximumSpeedLimit5End": 20,
        "Prohibitory_MaximumSpeedLimit5Begin": 21,
        "Prohibitory_MaximumSpeedLimit10End": 22,
        "Prohibitory_MaximumSpeedLimit10Begin": 23,
        "Prohibitory_MaximumSpeedLimit15End": 24,
        "Prohibitory_MaximumSpeedLimit15Begin": 25,
        "Prohibitory_MaximumSpeedLimit20Begin": 26,
        "Prohibitory_MaximumSpeedLimit20End": 27,
        "Prohibitory_MaximumSpeedLimit25End": 28,
        "Prohibitory_MaximumSpeedLimit25Begin": 29,
        "Prohibitory_MaximumSpeedLimit30End": 30,
        "Prohibitory_MaximumSpeedLimit30Begin": 31,
        "Prohibitory_MaximumSpeedLimit35End": 32,
        "Prohibitory_MaximumSpeedLimit35Begin": 33,
        "Prohibitory_MaximumSpeedLimit40End": 34,
        "Prohibitory_MaximumSpeedLimit40Begin": 35,
        "Prohibitory_MaximumSpeedLimit45End": 36,
        "Prohibitory_MaximumSpeedLimit45Begin": 37,
        "Prohibitory_MaximumSpeedLimit50Begin": 38,
        "Prohibitory_MaximumSpeedLimit50End": 39,
        "Prohibitory_MaximumSpeedLimit55Begin": 40,
        "Prohibitory_MaximumSpeedLimit55End": 41,
        "Prohibitory_MaximumSpeedLimit60Begin": 42,
        "Prohibitory_MaximumSpeedLimit60End": 43,
        "Prohibitory_MaximumSpeedLimit65Begin": 44,
        "Prohibitory_MaximumSpeedLimit65End": 45,
        "Prohibitory_MaximumSpeedLimit70Begin": 46,
        "Prohibitory_MaximumSpeedLimit70End": 47,
        "Prohibitory_MaximumSpeedLimit75End": 48,
        "Prohibitory_MaximumSpeedLimit75Begin": 49,
        "Prohibitory_MaximumSpeedLimit80Begin": 50,
        "Prohibitory_MaximumSpeedLimit80End": 51,
        "Prohibitory_MaximumSpeedLimit85Begin": 52,
        "Prohibitory_MaximumSpeedLimit85End": 53,
        "Prohibitory_MaximumSpeedLimit90Begin": 54,
        "Prohibitory_MaximumSpeedLimit90End": 55,
        "Prohibitory_MaximumSpeedLimit95Begin": 56,
        "Prohibitory_MaximumSpeedLimit95End": 57,
        "Prohibitory_MaximumSpeedLimit100End": 58,
        "Prohibitory_MaximumSpeedLimit100Begin": 59,
        "Prohibitory_MaximumSpeedLimit105End": 60,
        "Prohibitory_MaximumSpeedLimit105Begin": 61,
        "Prohibitory_MaximumSpeedLimit110End": 62,
        "Prohibitory_MaximumSpeedLimit110Begin": 63,
        "Prohibitory_MaximumSpeedLimit115Begin": 64,
        "Prohibitory_MaximumSpeedLimit115End": 65,
        "Prohibitory_MaximumSpeedLimit120End": 66,
        "Prohibitory_MaximumSpeedLimit120Begin": 67,
        "Prohibitory_MaximumSpeedLimit125Begin": 68,
        "Prohibitory_MaximumSpeedLimit125End": 69,
        "Prohibitory_MaximumSpeedLimit130End": 70,
        "Prohibitory_MaximumSpeedLimit130Begin": 71,
        "Prohibitory_NoEntry": 72,
        "Prohibitory_NoOvertakingBegin": 73,
        "Prohibitory_NoOvertakingEnd": 74,
        "Prohibitory_NoParking": 75,
        "Prohibitory_NoStopping": 76,
        "Prohibitory_NoTurn": 77,
        "Prohibitory_NoUTurn": 78,
        "Prohibitory_RoadClosed": 79,
        "Prohibitory_SpeedLimitZone5End": 80,
        "Prohibitory_SpeedLimitZone5Begin": 81,
        "Prohibitory_SpeedLimitZone10Begin": 82,
        "Prohibitory_SpeedLimitZone10End": 83,
        "Prohibitory_SpeedLimitZone15End": 84,
        "Prohibitory_SpeedLimitZone15Begin": 85,
        "Prohibitory_SpeedLimitZone20Begin": 86,
        "Prohibitory_SpeedLimitZone20End": 87,
        "Prohibitory_SpeedLimitZone25End": 88,
        "Prohibitory_SpeedLimitZone25Begin": 89,
        "Prohibitory_SpeedLimitZone30End": 90,
        "Prohibitory_SpeedLimitZone30Begin": 91,
        "Prohibitory_SpeedLimitZone35End": 92,
        "Prohibitory_SpeedLimitZone35Begin": 93,
        "Prohibitory_SpeedLimitZone40End": 94,
        "Prohibitory_SpeedLimitZone40Begin": 95,
        "Prohibitory_SpeedLimitZone45Begin": 96,
        "Prohibitory_SpeedLimitZone45End": 97,
        "Prohibitory_SpeedLimitZone50Begin": 98,
        "Prohibitory_SpeedLimitZone50End": 99,
        "Prohibitory_SpeedLimitZone55End": 100,
        "Prohibitory_SpeedLimitZone55Begin": 101,
        "Prohibitory_SpeedLimitZone60End": 102,
        "Prohibitory_SpeedLimitZone60Begin": 103,
        "Prohibitory_SpeedLimitZone65End": 104,
        "Prohibitory_SpeedLimitZone65Begin": 105,
        "Prohibitory_SpeedLimitZone70End": 106,
        "Prohibitory_SpeedLimitZone70Begin": 107,
        "Prohibitory_SpeedLimitZone75End": 108,
        "Prohibitory_SpeedLimitZone75Begin": 109,
        "Prohibitory_SpeedLimitZone80Begin": 110,
        "Prohibitory_SpeedLimitZone80End": 111,
        "Prohibitory_SpeedLimitZone85End": 112,
        "Prohibitory_SpeedLimitZone85Begin": 113,
        "Prohibitory_SpeedLimitZone90Begin": 114,
        "Prohibitory_SpeedLimitZone90End": 115,
        "Prohibitory_SpeedLimitZone95Begin": 116,
        "Prohibitory_SpeedLimitZone95End": 117,
        "Prohibitory_SpeedLimitZone100End": 118,
        "Prohibitory_SpeedLimitZone100Begin": 119,
        "Prohibitory_SpeedLimitZone105End": 120,
        "Prohibitory_SpeedLimitZone105Begin": 121,
        "Prohibitory_SpeedLimitZone110End": 122,
        "Prohibitory_SpeedLimitZone110Begin": 123,
        "Prohibitory_SpeedLimitZone115Begin": 124,
        "Prohibitory_SpeedLimitZone115End": 125,
        "Prohibitory_SpeedLimitZone120Begin": 126,
        "Prohibitory_SpeedLimitZone120End": 127,
        "Prohibitory_SpeedLimitZone125Begin": 128,
        "Prohibitory_SpeedLimitZone125End": 129,
        "Prohibitory_SpeedLimitZone130End": 130,
        "Prohibitory_SpeedLimitZone130Begin": 131,
        "RoadType_MotorwayBegin": 132,
        "RoadType_MotorwayEnd": 133,
        "Special_VulnurableRoadUserCrossing": 134,
        "Special_VulnurableRoadUserPathWay": 135,
        "Warning_Animal": 136,
        "Warning_Children": 137,
        "Warning_CongestionAhead": 138,
        "Warning_Crossroads": 139,
        "Warning_Crossing": 140,
        "Warning_Curve": 141,
        "Warning_Cyclists": 142,
        "Warning_DoubleCurve": 143,
        "Warning_GenericWarning": 144,
        "Warning_MergingTraffic": 145,
        "Warning_RoadBump": 146,
        "Warning_RoadWorkEnd": 147,
        "Warning_RoadWorkBegin": 148,
        "Warning_RoadNarrows": 149,
        "Warning_RoughRoad": 150,
        "Warning_Roundabout": 151,
        "Warning_Slippery": 152,
        "Warning_TrafficSignalAhead": 153,
        "Warning_TunnelAhead": 154,
        "Warning_TwoWayTraffic": 155,
    }

    for annotation in data:
        geometry = annotation['geometry']['coordinates']
        label_class = annotation['properties']['class']

        # Get class ID from hardcoded mappings
        class_id = class_mappings.get(label_class)

        if class_id is not None:
            # Calculate normalized center coordinates
            normalized_x_center, normalized_y_center = calculate_normalized_center(geometry, image_width, image_height)

            # Calculate normalized bounding box width and height and round to 5 decimal places
            width = round((geometry[1][0] - geometry[0][0]) / image_width, 5)
            height = round((geometry[2][1] - geometry[1][1]) / image_height, 5)

            # Append YOLO formatted label to the list
            yolo_labels.append(f"{class_id} {normalized_x_center} {normalized_y_center} {width} {height}")
        else:
            # If class is 'Unclear', assign class ID as -1
            normalized_x_center, normalized_y_center = calculate_normalized_center(geometry, image_width, image_height)
            width = round((geometry[1][0] - geometry[0][0]) / image_width, 5)
            height = round((geometry[2][1] - geometry[1][1]) / image_height, 5)
            yolo_labels.append(f"-1 {normalized_x_center} {normalized_y_center} {width} {height}")

    return yolo_labels

def main():
    # Example image dimensions (replace with actual dimensions)
    image_width = 3848
    image_height = 2168

    # Directory containing JSON files
    input_directory = r'/data_repo/u30r47/datasets/zod/train/labels_json'

    # Output directory for YOLO formatted labels
    output_directory = r'/data_repo/u30r47/datasets/zod/frames/labels/'

    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith("annotations/traffic_signs.json"):
            input_path = os.path.join(input_directory, filename)
            print(f"Processing file: {input_path}")

            # Open the JSON file and load data
            with open(input_path) as f:
                data = json.load(f)

            # Convert data to YOLO format
            yolo_labels = convert_to_yolo_format(data, image_width, image_height)

            # Save YOLO formatted labels to a text file in the output directory
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(output_directory, output_filename)
            with open(output_path, "w") as yolo_labels_file:
                for label in yolo_labels:
                    yolo_labels_file.write(label + "\n")

            print(f"YOLO formatted labels saved to {output_path}")

if __name__ == "__main__":
    main()



# def main():
#     # Example image dimensions (replace with actual dimensions)
#     image_width = 3848
#     image_height = 2168
#
#     # Input path to JSON file
#     input_path = "/data_repo/zod_new_download/single_frames/087912/annotations/traffic_signs.json"
#
#     # Open the JSON file and load data
#     with open(input_path) as f:
#         data = json.load(f)
#
#     # Convert data to YOLO format
#     yolo_labels = convert_to_yolo_format(data, image_width, image_height)
#
#     # Output path for YOLO formatted labels
#     output_path = "/data_repo/u30r47/datasets/zod/frames/labels/087912.txt"
#
#     # Save YOLO formatted labels to a text file
#     with open(output_path, "w") as yolo_labels_file:
#         for label in yolo_labels:
#             yolo_labels_file.write(label + "\n")
#
#     print(f"YOLO formatted labels saved to {output_path}")
#
# if __name__ == "__main__":
#     main()