import streamlit as st
import pandas as pd
import numpy as np
import re
st.set_page_config(layout='wide')
st.title('Plot allele frequency column from vcf file')
mvfe=st.file_uploader('Upload master variant file extreme here',type=['txt','maf','table'])
onlysnps=st.checkbox('only SNPs')
usegenomicCoordinate=st.checkbox('Use genomic coordinates instead of indices')
colorselection=st.radio('color points using:', ['Gene','DBSNP'])

if mvfe != None:
    st.write(mvfe.name)
    if mvfe.type == "text/plain":
        st.write('reading text file')
        chart_data = pd.read_table(mvfe,sep='\t')
    elif re.findall('table',mvfe.name):
        st.write('reading table file')
        chart_data = pd.read_table(mvfe,sep='\t',skiprows=1)    
        chart_data['AF']=chart_data['allele_frequency'] 
        chart_data['POS']=chart_data['position']
        chart_data['GENE']=chart_data['alt_count']
        chart_data['CHROM']=chart_data['contig']
    else:
        st.write('reading maf file')
        chart_data = pd.read_csv(mvfe,sep='\t',skiprows=1)    
        chart_data['AF']=chart_data['DP4'].str.split(',',expand=True).astype(int).apply(lambda x: x[2:4].sum()/x.sum(),axis=1) 
        chart_data['POS']=chart_data['Start_Position']
        chart_data['GENE']=chart_data['Hugo_Symbol']
        chart_data['CHROM']=chart_data['Chromosome']
    if onlysnps:
        chart_data=chart_data.iloc[np.where(chart_data['rsID'].str.contains('rs'))[0]]
        
    chart_data['ind']=  chart_data['POS']
    if colorselection=='Gene':    
        chart_data['gene_v_snp']=[str(y) for y in chart_data['GENE']] 
    else:    
        chart_data['gene_v_snp']=[str(y) for y in chart_data['dbSNP_RS']]    
        
    # Display a scatterplot chart  
    cola,colb,colc= st.columns(3)
    m=0
    for a in np.unique(chart_data['CHROM']):
        chrom = chart_data[chart_data['CHROM']==a]
        if not usegenomicCoordinate:
            chrom['ind']=np.arange(0,chrom.shape[0])
        chrom.reset_index(inplace=True)
        if m % 3 == 0:
            with cola:
                st.title(a+ ' x-axis index')
                st.scatter_chart(chrom,x='ind', y='AF',size=30,color='gene_v_snp')
        elif m % 3 == 1:    
            with colb:
                st.title(a+ ' x-axis index')
                st.scatter_chart(chrom,x='ind', y='AF',size=30,color='gene_v_snp')

        elif m % 3 == 2:  
               
            with colc:
                st.title(a+ ' x-axis index')
                st.scatter_chart(chrom,x='ind', y='AF',size=30,color='gene_v_snp')            
        m+=1        
    st.write(chart_data)   
