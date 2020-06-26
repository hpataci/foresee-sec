# foresee-sec
Causal Knowledge Extraction over SEC 10K Filing Documents



We get the tickers, and company information of SP500  from wikipedia. Used tickers, company identifiers, as the key input here.  A small sample was arranged here as 10k, for the entire sample please refer to SP500.CSV. 


1st stage inputs the tickers and provides Index links as output. 
2nd stage inputs the index links and provides 10-K links as output
3rd stage inputs the 10-K links and downloads corresponding html for each 10-K.
4th stage inputs HTML and downloads 1.A Risk factors section of the corresponding html of the 10-K.  Please see .txt file, once you run the code. 
 
Moreover, I created a Read log file to see which html was successfully read and extracted or failed to be extracted. So that, once the run ended, we can know which companies fail. 
 
In addition to that, I also created a broken pages list for companies I identified, that keeps giving failures due to formatting. I believe, this is because they have a different page structure. 
