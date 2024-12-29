from hyperon import MeTTa, SymbolAtom, ExpressionAtom, GroundedAtom
import os
import glob

metta = MeTTa()
metta.run(f"!(bind! &space (new-space))")

def load_dataset(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
    paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    for path in paths:
        print(f"Start loading dataset from '{path}'...")
        try:
            metta.run(f'''
                !(load-ascii &space {path})
                ''')
            print(metta.run(f"!(show &space)"))
        except Exception as e:
            print(f"Error loading dataset from '{path}': {e}")
    print(f"Finished loading {len(paths)} datasets.")

# Example usage:
try:
    dataset = load_dataset("./Data")
except Exception as e:
    print(f"An error occurred: {e}")

# 2 Points
def get_transcript(node):
    gene = node[0]  # Extract the gene identifier from the input node
    # print("gene: ", gene, "node: ", node)
    query = f"!(match &space (,(transcribed_to ({gene}) $transcript)) (,(transcribed_to ({gene}) $transcript)))"
    
    
    try:
        transcript = metta.run(query)
        return transcript
    except Exception as e:
        print(f"An error occurred while fetching transcripts: {e}")
        return None

    

#2 Points
def get_protein(node):
    # Extract the gene identifier from the input node
    gene = node[0]
    
    # Step 1: Transcribe the gene to get the transcript
    transcript_query = f"!(match &space (,(transcribed_to ({gene}) $transcript)) (,(transcribed_to ({gene}) $transcript)))"
    
    try:
        transcript_result = metta.run(transcript_query)
        transcript_result = get_transcript(node)
        if not transcript_result or not transcript_result[0]:
            print("No transcripts found for the given gene.")
            return None
        
        transcripts = []
        for exp in transcript_result[0]:
            if isinstance(exp, ExpressionAtom):
                transcript = exp.get_children()[1].get_children()[2]  # get_children method from ExpressionAtom class
                transcripts.append(transcript)        
        proteins = []
        for transcript in transcripts:
            
            transcript = str(transcript)[1:-1]
            protein_query =  f"!(match &space (,(translates_to ({transcript}) $protein)) (,(translates_to ({transcript}) $protein)))"
            protein_result = metta.run(protein_query)
            proteins.append(protein_result[0][0])
        

            
        
        return [proteins]if proteins else None
    
    except Exception as e:
        print(f"An error occurred while fetching proteins: {e}")
        return None




#6 Points
def metta_seralizer(metta_result):
    # Implement logic to convert the Metta output into a structured format  (e.g., a list of dictionaries) that can be easily serialized to JSON.
    result = []
    for expr in metta_result[0]:
        # print("expr: ", expr, "expr.children: ", expr.get_children())
        if isinstance(expr, ExpressionAtom):
            inner_expr = expr.get_children()[1]  # Access the inner expression
            if isinstance(inner_expr, ExpressionAtom):
                edge = str(inner_expr.get_children()[0])
                source = str(inner_expr.get_children()[1])
                target = str(inner_expr.get_children()[2])
                
                # Remove parentheses from source and target
                source = source[1:-1]  
                target = target[1:-1]
                
                result.append({
                    'edge': edge,
                    'source': source,
                    'target': target
                })
    return result


#1
transcript_result= (get_transcript(['gene ENSG00000166913']))
# print(transcript_result) 
# """
# Expected Output Format::
# # [[(, (transcribed_to (gene ENSG00000166913) (transcript ENST00000372839))), (, (transcribed_to (gene ENSG00000166913) (transcript ENST00000353703)))]]
# """ 

# #2
# protein_result= (get_protein(['gene ENSG00000166913']))
# print(protein_result) 
# """
# Expected Output Format::
# # [[(, (translates_to (transcript ENST00000353703) (protein P31946))), (, (translates_to (transcript ENST00000372839) (protein P31946)))]]
# """

#3
parsed_result = metta_seralizer(transcript_result)
print(parsed_result) 


"""
Expected Output Format:
[
    {'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}
]
"""
