from tkinter import *
import cv2
import pyzbar.pyzbar as pyzbar
def scan_book_qr(book_entry):
        # Create a video capture object
    cap = cv2.VideoCapture(0)
    
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        
        # Display the frame
        cv2.imshow('QR Code Scanner', frame)
        
        # Detect QR codes
        barcodes = pyzbar.decode(frame)
        
        # Check if any QR code is detected
        if barcodes:
            # Extract the data from the QR code
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                
                # Insert the QR code data into the entry widget
                book_entry.delete(0, END)
                book_entry.insert(END, barcode_data)
                
            # Break the loop
            break
        
        # Check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object and close the windows
    cap.release()
    cv2.destroyAllWindows()
    
def scan_id_qr(ID_entry):
        # Create a video capture object
    cap = cv2.VideoCapture(0)
    
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        
        # Display the frame
        cv2.imshow('QR Code Scanner', frame)
        
        # Detect QR codes
        barcodes = pyzbar.decode(frame)
        
        # Check if any QR code is detected
        if barcodes:
            # Extract the data from the QR code
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                
                # Insert the QR code data into the entry widget
                ID_entry.delete(0, END)
                ID_entry.insert(END, barcode_data)
                
            # Break the loop
            break
        
        # Check for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the video capture object and close the windows
    cap.release()
    cv2.destroyAllWindows()