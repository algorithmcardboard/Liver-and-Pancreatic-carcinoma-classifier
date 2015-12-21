#!/bin/bash
#PBS -l nodes=1:ppn=12
#PBS -l walltime=8:00:00
#PBS -l mem=164GB
#PBS -N svm_g_tissue_job
#PBS -M ac5901@nyu.edu,ajr619@nyu.edu
#PBS -j oe
#PBS -m e

module purge

SRCDIR=$HOME/workspace/Pancreatic-carcinoma-classifier/src
RUNDIR=$SCRATCH/Pancreatic-carcinoma-classifier/run-${PBS_JOBID/.*}
mkdir -p $RUNDIR

cd $PBS_O_WORKDIR

cp -R $SRCDIR/* $RUNDIR

cd $RUNDIR

module load virtualenv/12.1.1;
module load scipy/intel/0.16.0

virtualenv .venv

source .venv/bin/activate;

pip install -r requirements.txt

python -u pipeline/svmg_tissue_type.py
