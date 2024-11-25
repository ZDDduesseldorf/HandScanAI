from embeddings_utils import (
    preprocess_image,
    calculate_embedding,
    calculate_embeddings,
    calculate_concatenated_embedding,
)

from image_utils import load_image

from models_utils import build_densenet121_model, build_resnet50_model

### LOAD TEST IMAGES

path_to_images = "backend/embeddings/data/TestImages/"
random_images_names = [
    "Hand_0000002.jpg",
    "Hand_0000025.jpg",
    "Hand_0000048.jpg",
    "Hand_0000068.jpg",
    "Hand_0000088.jpg",
    "Hand_0000111.jpg",
    "Hand_0000144.jpg",
]
loaded_images = []
for name in random_images_names:
    loaded_images.append(load_image(name, path_to_images))

test_image = loaded_images[0]
print()
print("Image Tensor after Loading: \n")
print(test_image)


### LOAD MODEL
print()
print("Load Densenet-Model (print Classifier): \n")

densenet_model = build_densenet121_model()
print(densenet_model.classifier)  # expected: Identity-Layer

### PREPROCESS IMAGE
print()
print("Preprocess Image: \n")
preprocess_image(test_image)


## CALCULATE EMBEDDINGS

embedding_1 = calculate_embedding(
    random_images_names[0], build_densenet121_model(), path_to_images
)

print()
print("Embedding 1 Shape: \n")
print(embedding_1.shape)  # expected: 1024

# test if nine images result in nine embedding vectors
embeddings_list = calculate_embeddings(
    random_images_names, build_densenet121_model(), path_to_images
)
print()
print("Embeddings list size: \n")
print(len(embeddings_list))

# test if nine images result in one super embedding of the size of 9216
super_embedding_test = calculate_concatenated_embedding(
    random_images_names, build_densenet121_model(), path_to_images
)

# print()
# print("Super-Embedding at the end: \n")
# print(super_embedding_test) # list of embedding-float, TODO: turn into tensor

print()
print("Super-Embedding shape, expected is torch.Size([1, 9216]) with 9 pictures: \n")
print(super_embedding_test.shape)  # expected: torch.Size([1, 9216])
print(super_embedding_test)


### RESNET test
print()
print("ResNet50 architecture")
# print(build_resnet50_model())

super_embedding_resnet_test = calculate_concatenated_embedding(
    random_images_names, build_resnet50_model(), path_to_images
)

print()
print(f"ResNet50: {super_embedding_resnet_test.shape}")  # tensor torch.Size([1, 9000])
print(f"ResNet50: {super_embedding_resnet_test}")
