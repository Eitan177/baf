import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(layout='wide')
st.title('Plot allele frequency column from vcf file')
mvfe=st.file_uploader('Upload master variant file extreme here')
onlysnps=st.checkbox('only SNPs')
usegenomicCoordinate=st.checkbox('Use genomic coordinates instead of indices')

if mvfe != None:
    chart_data = pd.read_table(mvfe,sep='\t')
    if onlysnps:

        st.write(mvfe)
        mvfe=mvfe.iloc[np.where(mvfe['rsID'].str.contains('rs'))[0]]
    # Display a scatterplot chart
    cola,colb,colc= st.columns(3)
    m=0
    for a in np.unique(chart_data['CHROM']):
        chrom = chart_data[chart_data['CHROM']==a]
        if not usegenomicCoordinate:
            chrom['ind']=np.arange(0,chrom.shape[0])
        else:
            chrom['ind']=  chrom['POS']
        chrom['gene']=[str(y) for y in chrom['GENE']] 
        chrom.reset_index(inplace=True)
        if m % 3 == 0:
            with cola:
                st.title(a+ ' x-axis index')
                st.scatter_chart(chrom,x='ind', y='AF',size=30,color='gene')
        elif m % 3 == 1:    
            with colb:
                st.title(a+ ' x-axis index')
                st.scatter_chart(chrom,x='ind', y='AF',size=30,color='gene')

        elif m % 3 == 2:  
               
            with colc:
                st.title(a+ ' x-axis index')
                st.scatter_chart(chrom,x='ind', y='AF',size=30,color='gene')            
        m+=1        
    st.write(chart_data)   
