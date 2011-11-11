class GATK(object):
    """
    encapsulates various members of the GATK pipeline
    """
    def __init__(self,config):
        """
        initialize with config values
        :param config: A config object
        """
        self.jarfile=config['GATK']['jarfile']
        self.reference=config['reference']
        self.dbsnp=config['dbsnp']
        
    def UnifiedGenotyper(self,bamfiles,metricsfile,vcffile,other_args=None):
        """
        run the UnifiedGenotyper
        :param bamfiles: bamfiles to run
        :param metricsfile: output metrics file
        :param vcffile: output vcf file
        :param other_args: put on command-line verbatim
        """
        if(other_args==None):
            other_args=''
        cmd = """java64 -Xmx2g -jar /usr/local/GATK/GenomeAnalysisTK.jar -T UnifiedGenotyper -R %s --dbsnp %s %s --metrics_file %s --out %s 
%s""" % (self.reference,self.dbsnp," ".join('-I '+ i for i in bamfiles),metricsfile,vcffile,other_args)
        return(cmd)
