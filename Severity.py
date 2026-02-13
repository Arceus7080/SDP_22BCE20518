import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_leaf_and_calculate_severity(image_path):
    # 1. Load the image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # For displaying with Matplotlib
    
    # 2. Convert to Grayscale and blur slightly to remove noise
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Apply Otsu's Thresholding
    # This automatically separates the foreground (leaf) from the background
    # Note: You may need cv2.THRESH_BINARY_INV instead depending on if your background is light or dark
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 4. Find Contours (outlines of shapes)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("No leaf found!")
        return
        
    # 5. Grab the largest contour (this is almost certainly our leaf)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # 6. Create a blank black mask and fill the leaf contour with white
    leaf_mask = np.zeros_like(gray)
    cv2.drawContours(leaf_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
    
    # 7. Apply the mask to the original image (The "Crop")
    # Everything outside the leaf becomes pure black (pixel value 0)
    isolated_leaf = cv2.bitwise_and(img_rgb, img_rgb, mask=leaf_mask)
    
    # ==========================================
    # NOW WE CALCULATE SEVERITY ON THE ISOLATED LEAF
    # ==========================================
    
    # Total Leaf Area: Count all non-zero pixels in the leaf_mask
    total_leaf_pixels = cv2.countNonZero(leaf_mask)
    
    # Disease Area: Let's assume disease spots are dark/brown.
    # We convert to HSV to find those specific colors inside our isolated leaf.
    hsv_leaf = cv2.cvtColor(isolated_leaf, cv2.COLOR_RGB2HSV)
    
    # Define color range for the disease (e.g., Apple Scab / Black Rot)
    # You will need to tweak these numbers based on your specific disease
    lower_disease_color = np.array([10, 50, 20])  # Dark brown/yellowish
    upper_disease_color = np.array([30, 255, 200]) 
    
    # Create a mask just for the diseased spots
    disease_mask = cv2.inRange(hsv_leaf, lower_disease_color, upper_disease_color)
    disease_pixels = cv2.countNonZero(disease_mask)
    
    # Calculate Final Severity
    severity_percentage = (disease_pixels / total_leaf_pixels) * 100
    
    # --- Visualization ---
    fig, arr = plt.subplots(1, 4, figsize=(20, 5))
    arr[0].imshow(img_rgb)
    arr[0].set_title("Original Image")
    
    arr[1].imshow(leaf_mask, cmap='gray')
    arr[1].set_title("1. Extracted Leaf Mask")
    
    arr[2].imshow(isolated_leaf)
    arr[2].set_title("2. Background Removed")
    
    arr[3].imshow(disease_mask, cmap='hot')
    arr[3].set_title(f"3. Disease Detected\nSeverity: {severity_percentage:.2f}%")
    
    plt.show()

# Run it on one of your test images!
# extract_leaf_and_calculate_severity('path/to/your/apple_scab_image.jpg')

extract_leaf_and_calculate_severity(r"C:\Users\Dbaiv\Desktop\SDP_Plant\Cherry_disease\valid\Cherry_(including_sour)___healthy\00a8e886-d172-4261-85e2-780b3c50ad4d___JR_HL 4156.JPG")