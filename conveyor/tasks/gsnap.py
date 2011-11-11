from conveyor.utils import safe_run
import os

class GSNAP(object):
    """
    Container for tasks related to GSNAP
    """

    def __init__(self,gmap_bin_directory=None):
        """
        Initialize a new GSNAP object
        
        :param gmap_bin_directory: To specify a specific location for gmap and gsnap binaries.  If not is specified, the executable from PATH is used
        """
        self.bin_dir = gmap_bin_directory
    
    
    def build_index(self,
                    genome,
                    fasta_files,
                    kmer=15,
                    genome_directory=None):
        """
        Build an index using gmap_build.
        
        :param genome: The name of the genome, like 'hg19'
        :param fasta_files: A list of the fasta files to be included in the index
        :param kmer: The kmer size to use; default 15
        :param genome_directory: The genome directory to install to.  If None is specified, the executable on the PATH is used."""
        cmd = ""
        if(self.bin_dir is None):
            cmd = "gmap_build "
        else:
            cmd = os.path.join(self.bin_dir,"gmap_build ")
        if(not isinstance(fasta_files,list)):
            fasta_files = [fasta_files]
        cmd += "-d %s -d %d %s" % (genome,kmer,' '.join(fasta_files))
        safe_run(cmd)
        cmd = "make -f Makefile.%s coords"
        safe_run(cmd)
        cmd = "make -f Makefile.%s gmapdb"
        safe_run(cmd)
        cmd = "make -f Makefile.%s install"
        safe_run(cmd)
        return True

    def align_rna(self,
                  genome,
                  fastq,
                  outfile,
                  threads=1,
                  other_params='-B 5',
                  splicefile=None,
                  novel_splice=True,
                  genome_directory=None,
                  rg_sample=None,
                  rg_id=None,
                  rg_library=None,
                  rg_platform='Illumina',
                  samtools="samtools"):
        """
        Run gsnap RNA alignment.  Output is a sorted BAM file.

        :param genome: the genome name to use (match the original build index genome name)
        :param fastq: the fastq file or fastq files to align.  If files end in .gz, --gunzip will be added to command-line.
        :param outfile: the name of the output file
        :param threads: the number of threads to use [int]
        :param other_params: string inserted into the command-line with other parameters not otherwise captured
        :param splicefile: The name of the splicing file to use
        :param novel_splice: Should novel splice sites be sought, default True
        :param genome_directory: The genome directory to use.  If None, the default genome directory is used.
        :param rg_sample: Put into the RG-SM field in the SAM output
        :param rg_id: Put into the RG-ID field in the SAM output
        :param rg_library: Put into the RG-LB field in the SAM output
        :param rg_platform: Put into the RG-PL field in the SAM output
        :param samtools: full path to samtools executable. Default "samtools".
        """
        if(self.bin_dir is None):
            cmd = "gsnap "
        else:
            cmd = os.path.join(self.bin_dir,"gsnap ")
        cmd += "-t %d " % threads
        if(genome_directory is not None):
            cmd += "-D %s " % genome_directory
        if(other_params is not None):
            cmd += other_params + " "
        if(splicefile is not None):
            cmd += "-s %s " % splicefile
        if(novel_splice):
            cmd += "-N "
        cmd += "-d %s " % genome
        if(rg_id is not None):
            cmd += "--read-group-id=%s --read-group-platform=%s " % (rg_id,rg_platform)
            if(rg_library is not None):
                cmd += "--read-group-library=%s " % rg_library
            if(rg_sample is not None):
                cmd += "--read-group-sample=%s " % rg_sample
        if(isinstance(fastq,tuple) or isinstance(fastq,list)):
            if(len(fastq)>2):
                raise Exception('Too many fastq files given: %s' % str(fastq))
        else:
            fastq=[fastq]
        if(fastq[0].endswith('.gz')):
            cmd += '--gunzip '
        cmd += ' '.join(fastq)

        cmd += " | samtools view -bS - | samtools sort -m 5000000000 %s " % outfile
        res=safe_run(cmd)
        return res
