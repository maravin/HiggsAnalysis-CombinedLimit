from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import re

class FA3Heshy(PhysicsModel):
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        #all from https://twiki.cern.ch/twiki/bin/viewauth/CMS/Run2MCProductionforHiggsProperties
        #note have to use different numbers for other anomalous coupligns, these are only for fa3
        xsecs = {
          "sigma1_HZZ": 290.58626,
          "sigma3_HZZ": 581.17253,
          "sigma1_VBF": 968.674,
          "sigma3_VBF": 10909.54,
          "sigma1_ZH":  9022.36,
          "sigma3_ZH":  434763.7,
          "sigma1_WH":  30998.54,
          "sigma3_WH":  2028656
        }

        self.modelBuilder.doVar("CMS_zz4l_fai1[0.0,0.0,1]")  #Name is consistent with HZZ analysis.  Don't change it!
        self.modelBuilder.doVar("muV[1.0,0.0,2.0]")
        #self.modelBuilder.doVar("muf[1.0,0.0,10.0]")
        self.modelBuilder.doVar('expr::a1("sqrt(1-abs(@0))", CMS_zz4l_fai1)')
        self.modelBuilder.doVar('expr::a3("sqrt(@0)", CMS_zz4l_fai1)')
        #self.modelBuilder.doVar('expr::a3("(@0>0 ? 1 : -1) * sqrt(abs(@0) * {sigma1_HZZ}/{sigma3_HZZ})", CMS_zz4l_fai1)'.format(**xsecs))
        self.modelBuilder.doSet("POI","CMS_zz4l_fai1,muV")
        #self.modelBuilder.out.var("muf").setAttribute("flatParam")

        self.modelBuilder.factory_('expr::smCoupling_VBF("@0*@1**2", muV,a1)'.format(**xsecs))
        self.modelBuilder.factory_('expr::bsmCoupling_VBF("@0*@1**2*{sigma3_VBF}/{sigma1_VBF}", muV,a3)'.format(**xsecs))
        self.modelBuilder.factory_('expr::smCoupling_ZH("@0*@1**2", muV,a1)'.format(**xsecs))
        self.modelBuilder.factory_('expr::bsmCoupling_ZH("@0*@1**2*{sigma3_ZH}/{sigma1_ZH}", muV,a3)'.format(**xsecs))
        self.modelBuilder.factory_('expr::smCoupling_WH("@0*@1**2", muV,a1)'.format(**xsecs))
        self.modelBuilder.factory_('expr::bsmCoupling_WH("@0*@1**2*{sigma3_WH}/{sigma1_WH}", muV,a3)'.format(**xsecs))
        #interference will look like this:
        #self.modelBuilder.factory_('expr::intCoupling_VBF("@0*@1*@2 / sqrt({sigma1_VBF}*{sigma3_VBF})", muV,a1,ai)'.format(**xsecs))
    def getYieldScale(self,bin,process):
        if process in ["ggH_htt",]:
            return 'muV'
        if process in ["qqH_htt",]:
            return 'smCoupling_VBF'
        if process in ["ZH_htt",]:
            return 'smCoupling_ZH'
        if process in ["WH_htt",]:
            return 'smCoupling_WH'
        if process in ["qqH_htt_0M",]:
            return 'bsmCoupling_VBF'
        if process in ["ZH_htt_0M",]:
            return 'bsmCoupling_ZH'
        if process in ["WH_htt_0M",]:
            return 'bsmCoupling_WH'
        return 1

FA3Heshy = FA3Heshy()
