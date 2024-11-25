from embeddings_utils import (
    preprocess_image,
    calculate_embedding,
    calculate_embeddings,
    calculate_embeddings_from_path,
)

from image_utils import load_image

from models_utils import load_model, CNNModel

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
print(test_image.shape)


### LOAD MODEL
print()
print("Load Densenet-Model (print Classifier): \n")

densenet_model = load_model()
print(densenet_model.classifier)  # expected: Identity-Layer

### PREPROCESS IMAGE
print()
print("Preprocess Image: \n")
preprocess_image(test_image)


## CALCULATE EMBEDDINGS

embedding_1 = calculate_embedding(loaded_images[0], load_model())

print()
print("Embedding 1 Shape: \n")
print(embedding_1.shape)  # expected: 1024

# test if nine images result in nine embedding vectors
embeddings_list_loaded = calculate_embeddings(loaded_images, load_model())
print()
print("Embeddings list size: \n")
print(len(embeddings_list_loaded))

# test if nine images result in nine embedding vectors
embeddings_list = calculate_embeddings_from_path(random_images_names, path_to_images, load_model())
print()
print("Embeddings list size: \n")
print(len(embeddings_list))


### RESNET test
print()
print("ResNet50 architecture")
# print(build_resnet50_model())

embeddings_array_resnet = calculate_embeddings(loaded_images, load_model(CNNModel.RESNET_50))

print()
print(f"ResNet50: {len(embeddings_array_resnet)}")
