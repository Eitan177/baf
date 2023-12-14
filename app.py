import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(layout='wide')
st.title('Plot allele frequency column from vcf file')
mvfe=st.file_uploader('Upload master variant file extreme here',type=['txt','maf'])
onlysnps=st.checkbox('only SNPs')
usegenomicCoordinate=st.checkbox('Use genomic coordinates instead of indices')

if mvfe != None:
    if uploaded_file.type == "text/csv":
        st.write('reading text file')
        chart_data = pd.read_table(mvfe,sep='\t')
    else:
        st.write('reading maf file')
        chart_data = pd.read_csv(mvfe,sep='\t',skiprows=1)    
        chart_data['AF']=chart_data['DP4'].str.split(',',expand=True).astype(int).apply(lambda x: x[2:4].sum()/x.sum(),axis=1) 
        chart_data['POS']=chart_data['Start_Position']
        chart_data['GENE']=chart_data['Hugo_Symbol']
        chart_data['CHROM']=chart_data['Chromosome']
    if onlysnps:
        chart_data=chart_data.iloc[np.where(chart_data['rsID'].str.contains('rs'))[0]]
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
