from embeddings_utils import (
    preprocess_image,
    build_densenet_model,
    calculate_embedding,
    calculate_embeddings,
    calculate_concatenated_embedding,
)

from image_utils import load_image


### LOAD TEST IMAGES

path_to_images = "embeddings/embeddings/data/Hands/Hands/"
random_images_names = [
    "Hand_0000002.jpg",
    "Hand_0000025.jpg",
    "Hand_0000048.jpg",
    "Hand_0000068.jpg",
    "Hand_0000088.jpg",
    "Hand_0000111.jpg",
    "Hand_0000144.jpg",
    "Hand_0000171.jpg",
    "Hand_0000200.jpg",
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

densenet_model = build_densenet_model()
print(densenet_model.classifier)  # expected: Identity-Layer

### PREPROCESS IMAGE
print()
print("Preprocess Image: \n")
preprocess_image(test_image)


## CALCULATE EMBEDDINGS

embedding_1 = calculate_embedding(
    random_images_names[0], build_densenet_model(), path_to_images
)

print()
print("Embedding 1 Shape: \n")
print(embedding_1.shape)  # expected: 1024

# test if nine images result in nine embedding vectors
embeddings_list = calculate_embeddings(random_images_names, path_to_images)
print()
print("Embeddings list size: \n")
print(len(embeddings_list))

# test if nine images result in one super embedding of the size of 9216
super_embedding_test = calculate_concatenated_embedding(
    random_images_names, path_to_images
)

# print()
# print("Super-Embedding at the end: \n")
# print(super_embedding_test) # list of embedding-float, TODO: turn into tensor

print()
print("Super-Embedding length, expected is 9216 with 9 pictures: \n")
print(len(super_embedding_test))  # expected: 9216
