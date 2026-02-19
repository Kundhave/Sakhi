const express = require('express');
const router = express.Router();
const { generateGroupReport, generateMemberReport } = require('../../services/pdfReport');

// GET group credit report as PDF
router.get('/group/:groupId', async (req, res) => {
  try {
    const pdf = await generateGroupReport(req.params.groupId);
    res.set({
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="sakhi-group-report-${req.params.groupId}.pdf"`,
      'Content-Length': pdf.length,
    });
    res.send(pdf);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET individual member report as PDF
router.get('/member/:memberId', async (req, res) => {
  try {
    const pdf = await generateMemberReport(req.params.memberId);
    res.set({
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="sakhi-member-report-${req.params.memberId}.pdf"`,
      'Content-Length': pdf.length,
    });
    res.send(pdf);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
