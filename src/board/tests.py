from django.test import TestCase
from django.urls import reverse
from .models import EntityStatePDU


class BoardViewsTest(TestCase):
    def test_dashboard_renders(self):
        """Verify the live dashboard page loads correctly.

        .. test_case:: Dashboard renders live stream summary
           :id: TC_DASHBOARD_001
           :tests: SPEC_CONNECTION_INFORMATION, REQ_DIS_INVESTIGATION_TOOLS
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DIS Live Stream')

    def test_pdu_list_shows_record_count(self):
        """Verify the PDU list refresh component includes the summary count.

        .. test_case:: PDU list summary count
           :id: TC_PDU_LIST_001
           :tests: SPEC_MESSAGES_PAGE, REQ_DIS_INVESTIGATION_TOOLS
        """
        response = self.client.get(reverse('pdu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'total saved')
