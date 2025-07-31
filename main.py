from fastapi import FastAPI, HTTPException, Query, Request
from guessit import guessit
import traceback
from fastapi.responses import JSONResponse
from request_logger import RequestLogger

app = FastAPI(
    title="GuessIt API",
    description="API for guessing information from filenames using guessit",
    version="1.0.0"
)

# Initialize the request logger
request_logger = RequestLogger()

@app.get("/api/guess")
async def guess_filename(request: Request, it: str = Query(None, description="Filename to analyze")):
    """
    Analyze a filename using guessit and return the extracted information.
    
    Args:
        request: The FastAPI request object
        it: The filename to analyze
        
    Returns:
        JSON object with the guessit analysis result
        
    Raises:
        400: If the filename is not provided
        500: If there's an error during execution
    """
    # Check if filename is provided
    if not it:
        raise HTTPException(status_code=400, detail="Filename not provided")
    
    # Get the client's IP address
    client_ip = request.client.host
    
    try:
        # Use guessit to analyze the filename
        result = guessit(it)
        
        # Extract title, year, and type from the result
        title = result.get('title')
        year = result.get('year')
        media_type = result.get('type')
        
        # Log the request
        request_logger.log(
            filename=it,
            requester_ip=client_ip,
            title=title,
            year=year,
            type_=media_type
        )
        
        # Convert result to a serializable format
        serializable_result = {k: str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None))) else v 
                              for k, v in result.items()}
        return serializable_result
    except Exception as e:
        # Capture the error and return a 500 response
        error_detail = f"Error processing filename: {str(e)}"
        traceback.print_exc()  # Print traceback for debugging
        
        # Log the error
        request_logger.log(
            filename=it,
            requester_ip=client_ip,
            error=error_detail
        )
        
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint that verifies guessit is working correctly.
    
    Tests two specific filenames and checks if guessit correctly identifies them.
    
    Returns:
        200 with "healthy" message if both tests pass
        400 with "broken" message if any test fails
    """
    try:
        # Test case 1: Rick and Morty episode
        filename1 = "Rick.and.Morty.S08E07.Ricker.than.Fiction.1080p.MAX.WEB-DL.DDP5.1.H.264-FLUX.mkv"
        result1 = guessit(filename1)
        
        # Check if the first result is correct
        is_result1_correct = (
            result1.get('title') == 'Rick and Morty' and
            result1.get('season') == 8 and
            result1.get('episode') == 7 and
            result1.get('episode_title') == 'Ricker than Fiction' and
            result1.get('screen_size') == '1080p' and
            result1.get('source') == 'Web' and
            result1.get('audio_codec') == 'Dolby Digital Plus' and
            result1.get('video_codec') == 'H.264'
        )
        
        # Test case 2: Police Academy movie collection
        filename2 = "Prometheus (2012) 1080p Bluray OPUS 7.1 AV1-WhiskeyJack.mkv"
        result2 = guessit(filename2)
        
        # Check if the second result is correct
        is_result2_correct = (
            result2.get('title') == 'Prometheus' and
            result2.get('year') == 2012 and
            result2.get('screen_size') == '1080p' and
            result2.get('source') == 'Blu-ray' and
            result2.get('audio_codec') == 'Opus'
        )
        
        # Return appropriate response based on results
        if is_result1_correct and is_result2_correct:
            return JSONResponse(content={"message": "healthy"}, status_code=200)
        else:
            return JSONResponse(content={"message": "broken"}, status_code=400)
    except Exception as e:
        # If any error occurs, return broken status
        error_detail = f"Health check failed: {str(e)}"
        traceback.print_exc()  # Print traceback for debugging
        return JSONResponse(content={"message": "broken", "error": error_detail}, status_code=500)

@app.get("/api/statistics")
async def get_statistics(num_requests: int = Query(100, description="Number of recent requests to return")):
    """
    Get statistics about the requests made to the /api/guess endpoint.
    
    Args:
        num_requests: Number of recent requests to return. Defaults to 100.
        
    Returns:
        JSON object with statistics about the requests:
        - total: Total number of requests ever made to the API
        - total_24h: Total number of requests in the past 24 hours
        - recent_requests: List of the most recent N requests
    """
    try:
        stats = request_logger.get_statistics(num_requests)
        return stats
    except Exception as e:
        error_detail = f"Error retrieving statistics: {str(e)}"
        traceback.print_exc()  # Print traceback for debugging
        raise HTTPException(status_code=500, detail=error_detail)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)