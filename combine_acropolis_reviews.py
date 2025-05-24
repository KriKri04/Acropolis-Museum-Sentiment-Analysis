import csv
import os
from typing import List, Dict

def read_review_files(file_paths: List[str]) -> List[Dict]:
    """
    Read multiple review CSV files and combine their contents.
    
    Args:
        file_paths: List of paths to the review CSV files
        
    Returns:
        A list of review dictionaries
    """
    all_reviews = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if any(row.values()):  # Skip empty rows
                        # Add source file information
                        row['source_file'] = os.path.basename(file_path)
                        all_reviews.append(row)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    
    return all_reviews

def save_to_csv(reviews: List[Dict], output_file: str) -> None:
    """
    Save the review data to a CSV file.
    
    Args:
        reviews: List of review dictionaries
        output_file: Path to the output CSV file
    """
    if not reviews:
        print("No reviews to save.")
        return
    
    # Get all possible field names from all reviews
    fieldnames = set()
    for review in reviews:
        fieldnames.update(review.keys())
    
    # Ensure essential fields come first
    essential_fields = ['RATING', 'REVIEW_TEXT', 'source_file']
    ordered_fieldnames = [field for field in essential_fields if field in fieldnames]
    ordered_fieldnames.extend([field for field in fieldnames if field not in essential_fields])
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ordered_fieldnames)
        writer.writeheader()
        writer.writerows(reviews)
    
    print(f"Successfully saved {len(reviews)} reviews to {output_file}")

def main():
    # List of review data files
    review_files = [
        "tripadvisor_acropolis_museum.csv",
        "tripadvisor_acropolis_museum512.csv",
        "tripadvisor_acropolis_museum2269.csv"
    ]
    
    # You can add more files to this list if you have multiple CSV files
    # For example:
    # review_files.extend([
    #     "tripadvisor_acropilis_museum_part2.csv",
    #     "tripadvisor_acropilis_museum_part3.csv"
    # ])
    
    # Output CSV file name
    output_csv = "all_acropolis_reviews.csv"
    
    # Read all review data
    print("Reading review files...")
    all_reviews = read_review_files(review_files)
    
    # Print summary
    print(f"Total reviews found: {len(all_reviews)}")
    
    # Save to CSV
    save_to_csv(all_reviews, output_csv)
    
    # Calculate some basic statistics
    try:
        ratings = [float(review['RATING']) for review in all_reviews if review.get('RATING', '').strip()]
        review_texts = [review['REVIEW_TEXT'] for review in all_reviews if review.get('REVIEW_TEXT', '').strip()]
        
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        avg_review_length = sum(len(text) for text in review_texts) / len(review_texts) if review_texts else 0
        
        # Count ratings by star level
        rating_counts = {}
        for rating in ratings:
            rating_counts[rating] = rating_counts.get(rating, 0) + 1
        
        print("\nBasic Statistics:")
        print(f"Average Rating: {avg_rating:.2f} / 5.0")
        print(f"Average Review Length: {avg_review_length:.2f} characters")
        print("\nRating Distribution:")
        for rating in sorted(rating_counts.keys()):
            count = rating_counts[rating]
            percentage = (count / len(ratings)) * 100 if ratings else 0
            print(f"  {rating} stars: {count} reviews ({percentage:.1f}%)")
            
    except Exception as e:
        print(f"Error calculating statistics: {e}")

if __name__ == "__main__":
    main()